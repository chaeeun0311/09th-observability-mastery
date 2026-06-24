# OTel

**방식 1. Dockerfile에 직접 넣기**

```python
COPY opentelemetry-javaagent.jar /app/
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar"
```

- 애플리케이션 이미지 안에 Agent가 포함됨
- 이미지가 커지고, Agent 버전 바꾸려면 이미지 다시 빌드해야 함

**방식 2. Java Agent 직접 주입 (JVM 옵션)**

```python
java -javaagent:/path/to/opentelemetry-javaagent.jar -jar app.jar
```

- 실행 시점에 Agent를 붙이는 방식
- 컨테이너 환경에서는 환경변수로 전달

**방식 3. Init Container** 

- 애플리케이션 컨테이너가 뜨기 전에 Init Container가 먼저 실행
- Agent jar 파일을 공유 볼륨에 복사
- 애플리케이션 컨테이너가 그 볼륨을 마운트해서 사용
- 애플리케이션 이미지를 건드리지 않아도 됨

---

### 실제 적용 구조

```python
┌─────────────────────────────────────────┐
│  Pod                                    │
│                                         │
│  ┌─────────────────────┐                │
│  │  Init Container     │                │
│  │  otel-agent-init    │                │
│  │                     │                │
│  │  javaagent.jar 복사 │                │
│  │  → /otel/ 볼륨      │                │
│  └──────────┬──────────┘                │
│             │ 완료 후 종료              │
│             ▼                           │
│  ┌─────────────────────┐                │
│  │  App Container      │                │
│  │  linkat-dev-server  │                │
│  │                     │                │
│  │  /otel/javaagent.jar│                │
│  │  마운트해서 사용     │                │
│  │                     │                │
│  │  JAVA_TOOL_OPTIONS  │                │
│  │  = -javaagent:...   │                │
│  └──────────┬──────────┘                │
│             │                           │
│      emptyDir 볼륨 공유                 │
└─────────────────────────────────────────┘
         │ 추적·메트릭·로그
         ▼
┌─────────────────────────────────────────┐
│  OTel Collector                         │
│  monitoring 네임스페이스                 │
│  포트 4318 (HTTP/protobuf)              │
└─────────────────────────────────────────┘
```

---

### 설정

1.  **otel.enabled 플래그로 ON/OFF 가능**

```python
otel:
  enabled: true  # false로 바꾸면 OTel 없이 배포
```

-> 개발 환경은 켜고, 필요 없을 때는 끌 수 있어서 유연함

1.  **환경변수로 OTel 설정 전달**

```python
JAVA_TOOL_OPTIONS: "-javaagent:/otel/javaagent.jar"
OTEL_SERVICE_NAME: "linkat-dev-server"
OTEL_EXPORTER_OTLP_ENDPOINT: "http://otel-collector:4318"
OTEL_LOGS_EXPORTER: "otlp"
OTEL_METRICS_EXPORTER: "otlp"
OTEL_TRACES_EXPORTER: "otlp"
```

-> 로그 / 메트릭 / 추적 세 가지 모두 OTel Collector로 전달

1.  **ArgoCD로 자동 배포**
- ArgoCD가 GitHub 레포를 바라보고 있다가 변경사항 감지 시 자동 동기화
- `otel.enabled: true` 설정이 ArgoCD를 통해 자동으로 반영됨
- Image Updater가 최신 이미지 태그를 자동으로 업데이트

---

### Init Container 방식의 장점

- 애플리케이션 이미지 수정 없이 OTel 붙일 수 있음
- Agent 버전 업그레이드 시 Init Container 이미지만 바꾸면 됨
- `otel.enabled` 플래그로 쉽게 ON/OFF 가능
- 여러 서비스에 같은 방식으로 일관되게 적용 가능