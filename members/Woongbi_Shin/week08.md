## 0. 기본 정보

- 이름: 신웅비
- 주차: 8주차
- 선택 유형:
    - [ ] 책 범위 정리
    - [ ] 딥다이브 주제 정리
    - [ ] 실습 / 프로젝트 적용 정리
    - [x] 최종 회고 / 산출물 공유
- 주제: Observability 학습 회고와 운영 관점 정리

---

## 1. 이번 주 내용 한 줄 요약

> 8주차에는 지금까지 학습한 Observability 개념을 바탕으로, 장애 대응에서 어떤 데이터를 어떤 순서로 신뢰할 수 있는지와 관측 시스템 자체의 신뢰성이 왜 중요한지 회고했다.

---

## 2. 최종적으로 정리한 관점

이번 스터디를 통해 가장 크게 바뀐 관점은 “모니터링 도구를 붙이면 운영이 쉬워진다”가 아니라, “운영자가 판단할 수 있는 신뢰 가능한 증거 체계를 만들어야 한다”는 것이다.

처음에는 Observability를 metrics, logs, traces를 잘 수집하는 문제로 생각했다. 하지만 학습을 진행하면서 중요한 것은 단순 수집이 아니라, 장애 상황에서 다음 질문에 답할 수 있는 구조라는 생각이 들었다.

- 사용자가 느끼는 문제가 실제로 발생했는가?
- 문제가 언제부터 시작됐는가?
- 전체 서비스 문제인가, 특정 route나 dependency 문제인가?
- 에러가 증가한 것인가, latency만 증가한 것인가?
- 내가 보고 있는 지표가 실제 시스템 상태를 제대로 반영하고 있는가?
- 관측 데이터 자체가 유실되거나 지연되고 있지는 않은가?

결국 Observability는 “많이 보는 것”보다 “판단 가능한 증거를 남기는 것”에 가깝다고 이해했다.

---

## 3. 스터디에서 중요하게 남은 개념

### 3-1. Monitoring과 Observability의 차이

Monitoring은 이미 알고 있는 문제를 감지하는 데 강하다. 예를 들어 CPU가 90%를 넘었는지, 5xx 비율이 임계치를 넘었는지 확인하는 방식이다.

반면 Observability는 아직 원인을 모르는 문제를 외부 신호만으로 추론할 수 있게 만드는 능력이다. 단순히 알람이 울리는 것에서 끝나는 것이 아니라, 왜 그런 일이 발생했는지 탐색할 수 있어야 한다.

이 차이를 이해하면서 dashboard나 alert를 만들 때도 “이 그래프가 예쁜가?”보다 “장애 때 어떤 질문에 답할 수 있는가?”가 더 중요하다고 느꼈다.

### 3-2. Golden Signals

Latency, Traffic, Errors, Saturation 네 가지 지표는 서비스 상태를 판단하는 기본 언어가 된다.

- Traffic: 부하가 증가했는가?
- Latency: 사용자가 느끼는 지연이 증가했는가?
- Errors: 실패 비율이 증가했는가?
- Saturation: 시스템이 한계에 가까워졌는가?

이 네 가지를 같이 보면 장애의 방향을 좁힐 수 있다. 예를 들어 traffic은 그대로인데 latency만 증가하면 외부 부하보다는 내부 병목이나 dependency 문제를 의심할 수 있다. traffic 증가 이후 saturation이 높아지고 latency와 error가 따라 올라간다면 capacity 문제일 가능성이 커진다.

### 3-3. Metrics, Logs, Traces의 역할 분리

세 신호는 서로 대체 관계가 아니라 역할이 다르다.

| 신호 | 역할 | 장애 대응에서의 쓰임 |
|---|---|---|
| Metrics | 집계된 상태 | 이상 구간과 영향 범위 파악 |
| Traces | 요청 흐름 | 어느 구간에서 시간이 쓰였는지 확인 |
| Logs | 사건 기록 | 구체적인 에러, 상태, 입력 맥락 확인 |

장애 상황에서는 보통 metric으로 이상 구간을 찾고, trace로 요청 경로를 좁힌 뒤, log로 구체적인 에러와 상태를 확인하는 흐름이 자연스럽다고 느꼈다.

---

## 4. 7주차 정리와 이어지는 핵심: 관측 시스템 자체의 견고함

7주차에는 Observability를 보장하기 위한 telemetry pipeline의 견고함을 정리했다. 이 내용이 스터디 후반부에서 가장 인상 깊었다.

Trace, metric, log는 시스템에서 발생한 모든 사건의 원본이 아니다. 실제로는 다음과 같은 pipeline을 통과한 결과다.

```text
Application
→ SDK Queue / Processor
→ Sampler / Aggregation
→ Exporter
→ Collector
→ Backend Ingest
→ Index / Query
→ Dashboard / Alert
```

이 과정에서 데이터는 샘플링될 수 있고, 집계될 수 있고, 지연될 수 있고, 일부는 drop될 수 있다.

따라서 장애 상황에서 trace가 보이지 않는다고 해서 요청이 없었던 것은 아니다. metric이 조용하다고 해서 서비스가 정상이라는 뜻도 아니다. 관측 pipeline 자체가 막혔거나 유실을 시작했을 가능성도 있다.

이 관점에서 Observability는 애플리케이션을 관측하는 문제이면서 동시에, 관측 시스템 자체를 안정적으로 운영하는 문제라고 느꼈다.

---

## 5. 장애 상황에서 데이터를 보는 순서

스터디를 통해 정리한 장애 대응 흐름은 다음과 같다.

### 1단계. 사용자 영향 확인

먼저 실제 사용자 영향이 있는지 확인한다.

- latency가 증가했는가?
- error rate가 증가했는가?
- 특정 기능만 문제인가?
- 전체 서비스에 영향이 있는가?

이 단계에서는 Golden Signals가 가장 유용하다.

### 2단계. 시간 범위 확정

문제가 언제부터 시작됐는지 확인한다.

- 배포 시점과 겹치는가?
- 트래픽 변화와 겹치는가?
- 외부 dependency 장애 시간과 겹치는가?
- 특정 batch나 이벤트와 겹치는가?

시간 범위를 좁히면 trace와 log를 볼 때 탐색 비용이 크게 줄어든다.

### 3단계. 범위 좁히기

전체 서비스 문제인지 특정 route, 특정 dependency, 특정 worker 문제인지 나눈다.

- route별 latency
- status code별 error rate
- dependency latency
- queue depth
- runtime resource 사용량

이 단계에서는 dashboard가 단순한 그래프 모음이 아니라, 원인 범위를 좁히는 질문 순서가 되어야 한다.

### 4단계. Trace와 Log로 구체화

Metric으로 이상 구간과 범위를 좁힌 뒤 trace와 log를 본다.

Trace는 요청이 어느 구간에서 시간을 썼는지 보여주고, log는 그 시점의 구체적인 에러나 상태를 보여준다. 처음부터 log만 뒤지면 탐색 범위가 너무 넓기 때문에, metric → trace → log 순서가 더 효율적이라고 느꼈다.

### 5단계. 관측 데이터 자체를 의심하기

마지막으로, 내가 보는 데이터가 정상적으로 수집되고 있는지도 확인해야 한다.

- collector queue가 밀리고 있지 않은가?
- exporter failure가 증가하지 않았는가?
- backend ingest delay가 있지 않은가?
- dashboard query interval이나 alert evaluation이 너무 느리지 않은가?
- sampling 정책 때문에 중요한 trace가 빠지고 있지 않은가?

이 단계가 없으면 “조용한 dashboard”를 “정상 서비스”로 오해할 수 있다.

---

## 6. 실제 운영에 적용한다면 확인하고 싶은 체크리스트

### Dashboard

- 서비스별 Golden Signals가 한 화면에 있는가?
- p50, p95, p99 latency를 구분해서 볼 수 있는가?
- route 또는 operation별로 병목을 좁힐 수 있는가?
- dependency latency를 같이 볼 수 있는가?
- dashboard 변수(service, environment, interval, time range)가 명확한가?

### Metrics

- metric label에 user_id, request_id, session_id 같은 고카디널리티 값이 들어가지 않는가?
- raw URL 대신 route template을 쓰는가?
- service별 series 수를 모니터링하는가?
- histogram bucket이 SLO 임계값 근처에서 충분히 촘촘한가?

### Traces

- sampling 정책이 의도적으로 설정되어 있는가?
- error trace나 slow trace를 놓치지 않기 위한 전략이 있는가?
- trace context propagation이 서비스 간에 유지되는가?
- batch/fan-in/fan-out 구조에서 span link를 고려했는가?

### Logs

- trace id와 연동되어 검색 가능한가?
- 민감정보가 log body나 attribute로 나가지 않는가?
- authorization header, token, query string 등이 제거되는가?

### Telemetry Pipeline

- collector 자체 metric을 보고 있는가?
- dropped spans/logs/metrics를 알 수 있는가?
- exporter failure와 retry count를 보고 있는가?
- metric freshness와 alert latency에 대한 기대치가 있는가?
- 관측 시스템 장애가 애플리케이션 장애로 전파되지 않도록 설계했는가?

---

## 7. 스터디를 통해 배운 점

### 7-1. 좋은 dashboard는 질문의 순서다

Dashboard는 그래프를 많이 모아둔 화면이 아니라, 장애 상황에서 어떤 질문을 어떤 순서로 던질지 정리한 화면이어야 한다.

좋은 dashboard는 “지금 어디가 이상한가?”뿐 아니라 “다음에 어디를 봐야 하는가?”를 알려줘야 한다.

### 7-2. 지표는 원본이 아니라 해석된 결과다

Metric은 집계된 관점이고, trace는 샘플링된 증거이며, log는 수집 가능한 만큼만 남는 기록이다.

따라서 어떤 지표도 단독으로 진실이라고 볼 수 없다. 여러 신호를 연결해서 해석해야 하고, 그 신호가 만들어진 pipeline도 함께 이해해야 한다.

### 7-3. Observability도 신뢰성의 대상이다

서비스의 reliability만 중요한 것이 아니라, 서비스를 관측하는 시스템의 reliability도 중요하다.

관측 시스템이 느리거나, 유실되거나, backend quota에 막히거나, collector가 과부하 상태라면 장애 대응 자체가 흔들린다. Observability를 보장하려면 telemetry pipeline에도 SLO가 필요하다고 느꼈다.

### 7-4. 운영자는 도구보다 판단 기준이 필요하다

Prometheus, Grafana, OpenTelemetry 같은 도구는 중요하지만, 더 중요한 것은 어떤 기준으로 볼 것인지다.

- 어떤 latency percentile을 볼 것인가?
- 어떤 label을 허용할 것인가?
- 어떤 error를 사용자 영향으로 볼 것인가?
- 어떤 alert가 사람을 깨울 가치가 있는가?
- 어떤 데이터는 drop되어도 되고, 어떤 데이터는 별도 durable path가 필요한가?

이런 판단 기준이 없으면 도구를 붙여도 운영 품질이 크게 좋아지지 않는다.

---

## 8. 실제 사례로 연결해본 내용

이번 스터디에서 배운 내용을 실제 운영 상황에 연결해보면, Observability는 단순히 이론적인 개념이 아니라 장애 대응의 순서를 정리하는 도구에 가깝다고 느꼈다.

외부에 공개할 수 있는 수준으로 일반화하면, 다음과 같은 사례들이 있었다.

### 8-1. 서비스 Overview Dashboard 구성

특정 Node.js 기반 서비스의 운영 상태를 한 화면에서 보기 위해 Grafana Service Overview Dashboard를 구성했다.

이 dashboard는 단순히 그래프를 많이 모아두는 것이 아니라, 장애 상황에서 다음 질문을 빠르게 확인하기 위한 목적이었다.

- 요청량이 평소보다 늘었는가?
- error rate가 증가했는가?
- p50, p95, p99 latency 중 어디가 튀는가?
- 특정 route 또는 operation에 문제가 집중되는가?
- dependency latency가 같이 증가했는가?
- runtime resource 사용량이 같이 변했는가?

이 사례를 통해 좋은 dashboard는 “보여줄 수 있는 모든 지표의 모음”이 아니라 “장애 대응 질문의 순서”여야 한다는 점을 더 체감했다.

### 8-2. Node.js runtime memory 관측

운영 대시보드에서 Node.js runtime memory를 볼 때 `heapUsed`만으로는 충분하지 않다는 점도 확인했다.

예를 들어 파일, 이미지, HTTP client, 압축, 암호화처럼 Buffer를 많이 사용하는 경로에서는 JS heap보다 `rss`, `external`, `arrayBuffers`가 더 중요한 단서가 될 수 있다.

그래서 memory 문제를 볼 때는 다음 지표를 함께 봐야 한다고 정리했다.

| 지표 | 의미 |
|---|---|
| heapUsed | V8 JS heap에서 실제 사용 중인 메모리 |
| heapTotal | V8이 확보한 heap 전체 크기 |
| external | V8이 추적하는 native/external memory |
| arrayBuffers | ArrayBuffer / Buffer backing store |
| RSS | 프로세스가 OS에서 실제 점유하는 resident memory |

특히 `heapUsed`는 안정적인데 `RSS`나 `arrayBuffers`가 증가한다면, 일반적인 JS object leak이 아니라 Buffer/ArrayBuffer 계열 메모리 보유 문제를 의심해야 한다.

이때 Grafana metric과 heap snapshot을 비교할 수 있지만, 둘은 같은 메모리를 완전히 같은 방식으로 보여주는 것이 아니다. metric은 현재 프로세스의 계량값에 가깝고, heap snapshot은 JS object graph 관점의 분석 도구에 가깝다. 따라서 같은 PID, 같은 worker, 같은 시간대 기준으로 비교해야 한다.

### 8-3. Telemetry 송신 경로 검증

OpenTelemetry를 적용할 때는 애플리케이션이 실제로 telemetry를 내보내는지 먼저 검증하는 것도 중요했다.

운영 backend에 바로 연결하기 전에, 로컬 또는 분리된 환경에서 OTLP receiver를 띄워 trace, metric, log가 실제로 export되는지 확인할 수 있다. 이렇게 하면 문제가 생겼을 때 다음을 분리해서 볼 수 있다.

- 애플리케이션 계측이 안 된 것인지
- SDK/exporter 설정이 잘못된 것인지
- collector가 받지 못하는 것인지
- backend ingest/query 쪽 문제인지

이 사례는 “데이터가 안 보인다”는 상황을 바로 애플리케이션 문제로 단정하면 안 된다는 점과 연결된다. Observability pipeline에서는 데이터가 만들어지는 지점부터 dashboard에 보이는 지점까지 여러 단계가 있기 때문에, 어느 단계에서 끊겼는지 나눠서 봐야 한다.

### 8-4. 고카디널리티와 span name 정리

또 하나 중요했던 것은 span name과 metric label을 아무 값으로나 만들면 안 된다는 점이다.

예를 들어 raw URL, query string, user id, request id 같은 값이 metric label이나 span name에 들어가면 cardinality가 커지고 backend 비용과 query 성능에 영향을 줄 수 있다.

그래서 실제 서비스에 적용할 때는 다음과 같은 방향이 필요하다고 느꼈다.

- raw URL 대신 route template 사용
- 외부 HTTP 요청은 host 단위 등으로 정규화
- health check처럼 분석 가치가 낮은 요청은 제외
- user id, request id, session id는 metric label로 사용하지 않기
- 필요 이상으로 많은 span을 만드는 instrumentation은 비활성화 검토

이 사례는 Observability가 단순히 데이터를 많이 남기는 문제가 아니라, 운영 가능한 형태로 남기는 문제라는 점을 보여준다.

---

## 9. 최종 회고

8주 동안 Observability를 공부하면서, 운영에서 중요한 것은 문제가 발생하지 않는 시스템을 만드는 것뿐 아니라 문제가 발생했을 때 빠르게 이해할 수 있는 시스템을 만드는 것이라는 생각이 들었다.

장애는 결국 발생한다. 중요한 것은 그때 운영자가 어떤 증거를 보고, 어떤 순서로 가설을 세우고, 어디까지 확신할 수 있는지다.

이번 스터디 전에는 observability를 “모니터링 도구들의 묶음” 정도로 생각했다. 하지만 지금은 observability를 “장애 상황에서 시스템을 이해할 수 있게 만드는 신뢰성 체계”에 가깝게 보게 됐다.

그리고 이 신뢰성 체계는 애플리케이션 코드만으로 만들어지지 않는다. metric 설계, trace sampling, log 구조화, dashboard 구성, alert 정책, collector 운영, backend ingest, query latency까지 모두 연결되어야 한다.

가장 크게 남은 문장은 다음이다.

> Observability는 데이터를 많이 모으는 것이 아니라, 장애 상황에서 믿을 수 있는 증거를 남기는 것이다.

앞으로 실제 서비스를 운영하거나 개선할 때도 단순히 “Grafana dashboard를 만들었다”, “OpenTelemetry를 붙였다”에서 끝내지 않고, 이 데이터가 장애 상황에서 어떤 판단을 가능하게 하는지, 그리고 그 데이터를 운반하는 pipeline 자체가 충분히 견고한지까지 함께 보려고 한다.
