# 오픈텔레메트리(OpenTelemetry, OTel)

트레이스, 메트릭, 로그를 수집, 생성, 처리, 내보내기(Export)하는 과정을 표준화한 오픈소스 관측 가능성(Observability) 프레임워크

### 왜 오픈텔레메트리가 필요한가?

기존에 모니터링을 위해서는 프로메테우스, 데이터독, 예거등 도구 에이전트를 애플리케이션에 개별적으로 설치해야했다. 이로 인해서 모니터링 도구의 벤더에 종속되거나, 더욱 복잡한 관리가 필요했다.

오픈텔레메트리는 데이터를 수집하는 표준 규격을 제공한다. 오픈텔레메트리 표준 방식으로 데이터를 한 번만 생성해 두면, 이를 프로메테우스, 그라파나, 데이터독 등 원하는 모니터링 분석 백엔드로 자유롭게 보낼 수 있다.

### 주요 구성요소

1. API
    
    소스코드에 관측 기능을 주입하기 위해 데이터 형식을 정의하는 추상화된 인터페이스
    
2. SDK
    
    API를 실제도 구현한 언어별 라이브러리
    
3. Collector
    
    애플리케이션 인프라 외부에 독립된 프로세스로 띄우는 프록시 서버
    데이터를 받고(Receiver), 가공하고(Processor), 모니터링 서버에 보내는(Exporter) 역할을 수행한다.
    

---

# 실습

[오픈텔레메트리 데모](https://github.com/open-telemetry/opentelemetry-demo)

1. 헬름 저장소 추가 및 파일 준비

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
```

1. 프로메테우스 OTLP 수신 기능 켜기

```
kubectl edit deployment prometheus
```
<img width="1782" height="1208" alt="image" src="https://github.com/user-attachments/assets/645342ac-9233-48d8-a558-1dd42893f836" />

<img width="1786" height="1212" alt="image" src="https://github.com/user-attachments/assets/71c61bfb-217d-4b2a-bcfc-a57a8cf42b13" />

```
프로메테우스 다시 시작 (삭제시 다시 뜸)
kubectl delete pod prometheus-12***
```
otel-demo-values.yaml

```bash
# 1. 데모 내장 모니터링 컴포넌트 비활성화 (이미 클러스터에 존재하므로)
prometheus:
  enabled: false

grafana:
  enabled: false

jaeger:
  enabled: false

# 2. OpenTelemetry Collector 설정을 기존에 실행 중인 서비스로 라우팅
opentelemetry-collector:
  config:
    exporters:
      # 기존 Tempo 서비스로 트레이스(Traces) 데이터 전송 (gRPC 4317 포트)
      otlp/tempo:
        endpoint: "tempo:4317"
        tls:
          insecure: true

      # 기존 Prometheus 서비스로 메트릭(Metrics) 데이터 전송 (OTLP 수신 활성화 완료)
      otlphttp/prometheus:
        endpoint: "http://prometheus:9090/api/v1/otlp"
        tls:
          insecure: true

      # 기존 Loki 서비스로 로그(Logs) 데이터 전송 (3100 포트 OTLP 엔드포인트)
      otlphttp/loki:
        endpoint: "http://loki:3100/otlp"
        tls:
          insecure: true

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlp/tempo]
        metrics:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlphttp/prometheus]
        logs:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlphttp/loki]
```
이전까지 띄운 LGTM에 오픈텔레메트리 연결
