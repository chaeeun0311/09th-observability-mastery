## 1. 배경 및 목표
인프라 환경: k3s 단일 노드 미니 PC, ArgoCD (App of Apps 패턴으로 전체 인프라 선언형 관리)

### 아키텍처
```
[ App Layer ]                     [ Core Hub ]                [ Backend Storage ]        [ Visualization ]
       
+----------------------------+
| app-dev / app-prod         |
| (Spring Boot Pod)          |
|                            |
|  [OTel Java Agent]         |
|         |                  |
|         | (OTLP http)      |
|         +--:4318-----------+------------+
|                            |            |
|  [Logback JSON stdout]     |            |
+---------|------------------+            |
          |                               |
          v (Write to Node Disk)          v
   /var/log/pods/*.log                    |
          |                               |
          | (Disk Mount)                  |
          v                               v
+-----------------------------------------------------+
| OTel Collector (DaemonSet Mode)                     |
|                                                     |
|  +-----------------------------------------------+  |
|  | receivers:                                    |  |
|  |   otlp/http (:4318) <-- traces, metrics only  |  |
|  |   filelog (with file_storage extension) <-- logs |
|  +-------------------+---------------------------+  |
|                      |                              |
|  +-------------------|---------------------------+  |
|  | exporters:        |                           |  |
|  |   otlp/tempo      | (OTLP grpc :4317)         |  |
|  |   otlphttp/loki   | (OTLP http :3100)         |  |
|  |   prometheus      | (Prometheus Scrape :8889) |  |
|  +---|-------|-------|---------------------------+  |
+------|-------|-------|------------------------------+
       |       |       |
       |       |       +------------> +------------------------+
       |       |                      | Prometheus             |
       |       |                      | (Metrics Storage)      |
       |       |                      +-----------|------------+
       |       |                                  |
       |       +-------------------> +------------------------+   +-------------------+
       |                             | Loki                   |   | Grafana           |
       |                             | (Logs Storage)         |---|                   |
       |                             +-----------|------------+   |  - Trace To Log   |
       +-----------------------------+           |                |  - Log To Trace   |
                                    v            |                +-------------------+
                             +----------------+  |
                             | Tempo          |--+
                             | (Trace Storage)|
                             +----------------+
```

**신호별 수집 경로:**

- **Traces / Metrics**: OTel Java Agent -> OTLP/HTTP `:4318` -> OTel Collector -> Tempo / Prometheus
- **Logs**: Logback JSON stdout -> `/var/log/pods/` -> filelog receiver -> Loki
  - logs는 filelog 단일 경로만 사용 (OTLP logs 비활성화)
  - 이유: OTLP 경로는 trace_id가 structured metadata로만 저장되어 Grafana의 trace-log 연결 기능이 동작하지 않음
  - filelog로 JSON 전체를 수집하면 trace_id가 로그 텍스트에 포함되어 연결 가능

---

## 2. 겪은 문제

### filelog receiver 무한 루프 및 로그 누락

#### 증상

OTel Collector DaemonSet 배포 후 app 네임스페이스 로그가 전혀 수집되지 않음

#### 원인

클러스터 내에 44일간 방치된 OOMKilled 좀비 Pod가 5분마다 새 로그 파일을 생성 중   
-> filelog receiver는 디렉토리를 알파벳 순으로 스캔하는데 좀비 Pod의 네임스페이스 이름이 app 네임스페이스보다 알파벳 앞 순서였고, 5분마다 새 파일이 생겨 app 로그 파일 스캔 순서가 오지 못하는 Starvation 상태 발생

추가로 기본 설정에서는 Collector 재시작 시 `start_at: end` 동작으로 이전에 읽던 위치를 잃어 로그 누락 발생

#### 해결

- 좀비 Pod 및 불필요한 배포 전체 제거
- `file_storage` extension 도입으로 노드 디스크에 체크포인트 영구 저장

```yaml
extensions:
  file_storage:
    directory: /var/lib/otelcol/filelogreceiver

receivers:
  filelog:
    storage: file_storage  # 재시작 후 이전 위치부터 이어서 읽음
```


---

## 3. 아키텍처 고도화: OTel Operator 전환

### 기존 방식 (Init Container 직접 정의)

서비스마다 `deployment.yaml`에 init container와 10여 개의 환경변수를 하드코딩 필요

```yaml
# 기존: 각 서버 deployment.yaml에 직접 정의
initContainers:
  - name: otel-agent-init
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-java:latest
env:
  - name: JAVA_TOOL_OPTIONS
    value: "-javaagent:/otel/javaagent.jar"
  - name: OTEL_SERVICE_NAME
    value: "linkat-dev-server"
  # ... 10개 이상의 환경변수
```

### 개선 방식 (OpenTelemetry Operator)

cert-manager와 OpenTelemetry Operator를 도입하여 Instrumentation CR 하나로 중앙 관리

```yaml
# Instrumentation CR 하나로 모든 설정 중앙화
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: linkat-instrumentation
  namespace: opentelemetry-operator-system
spec:
  exporter:
    endpoint: http://otel-collector:4318
  java:
    env:
      - name: OTEL_LOGS_EXPORTER
        value: none
      # ...
```

```yaml
# 새 서버 추가 시 annotation 한 줄만 추가하면 끝
annotations:
  instrumentation.opentelemetry.io/inject-java: "opentelemetry-operator-system/linkat-instrumentation"
```

> `inject-java: "true"` 방식은 Pod와 같은 네임스페이스에서 CR을 찾기 때문에 다른 네임스페이스의 CR을 참조하려면 `"네임스페이스/CR이름"` 형식으로 명시 필요

---

## 4. Observability 관점에서 배운 점

### 데이터 경로는 단순하고 일관될수록 좋음

로그가 OTLP와 filelog 두 경로로 중복 수집되면서 같은 로그가 두 가지 형태로 Loki에 저장되어 trace-log 연결이 동작하지 않음 
-> 파이프라인이 복잡할수록 디버깅이 어려워짐

---

## 5. 개선해야 할 점

### 로그 노이즈 필터링

actuator health check 로그가 매초 Loki에 쌓이고 있어 추후 OTel Collector filter processor로 제거 진행하기 

```yaml
filter/drop-health:
  logs:
    log_record:
      - 'IsMatch(body, ".*actuator/health.*")'
```

### 데이터 보존 기간 미설정

Tempo, Loki 모두 기본 보존 기간으로 운영 중  
-> 로그와 트레이스가 쌓일수록 디스크를 계속 사용하여 retention policy 설정 필요 