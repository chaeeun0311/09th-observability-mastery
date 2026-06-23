## 0. 기본 정보

- 이름: 신웅비
- 주차: 7주차
- 선택 유형:
    - [ ] 책 범위 정리
    - [x] 딥다이브 주제 정리
    - [ ] 실습 / 프로젝트 적용 정리
- 주제: Observability를 보장하기 위한 Telemetry Pipeline의 견고함

---

## 1. 이번 주 내용 한 줄 요약

> Observability는 도구를 붙인다고 자동으로 보장되는 것이 아니라, telemetry를 생성·가공·전송·저장·조회하는 pipeline 자체가 견고해야 유지된다.

---

## 2. 정리한 배경

이번 주에는 OpenTelemetry를 “어떻게 설치하고 span을 찍는가”보다, Observability를 실제로 보장하려면 그 뒤에 있는 telemetry pipeline이 얼마나 견고해야 하는지 중심으로 정리했다.

처음에는 OpenTelemetry를 trace를 남기는 표준 라이브러리 정도로 생각하기 쉬웠다. 하지만 SDK 구조를 보면 OpenTelemetry는 단순 API가 아니라 sampler, processor, exporter, metric reader, log processor, resource, semantic convention, collector까지 이어지는 꽤 큰 생태계다. 결국 관측 가능성을 믿으려면 이 생태계의 각 구간이 안정적으로 동작해야 한다.

특히 장애 상황에서는 dashboard나 trace backend에 보이는 데이터가 시스템에서 발생한 모든 사건의 원본이라고 착각하면 위험하다. 실제로 우리가 보는 trace, metric, log는 여러 단계를 거치며 샘플링되고, 집계되고, 지연되고, 일부는 버려진 결과다. 따라서 Observability의 품질은 애플리케이션 코드뿐 아니라 이 데이터를 운반하는 시스템의 신뢰성에 크게 의존한다.

이번 정리의 핵심 문장은 다음과 같다.

> Trace는 진실이 아니라 샘플링된 증거다.

그리고 그 증거를 믿으려면 증거가 만들어지고 운반되는 pipeline 자체가 충분히 견고해야 한다.

---

## 3. Observability를 구성하는 Telemetry Runtime

Observability를 구현하는 도구들은 크게 API와 SDK, 그리고 외부 pipeline으로 나눠서 볼 수 있다. 여기서는 OpenTelemetry SDK를 예시로 삼아, 애플리케이션 내부에서 telemetry가 어떻게 만들어지고 처리되는지 정리했다.

### 3-1. API와 SDK의 분리

API는 라이브러리나 애플리케이션 코드가 instrumentation을 위해 호출하는 인터페이스다. 예를 들어 span을 만들거나 현재 context를 읽는 동작은 API를 통해 이루어진다.

반면 SDK는 실제 telemetry를 어떻게 처리할지 결정하는 구현체다. SDK는 다음과 같은 정책을 가진다.

- 어떤 trace를 수집할지 결정하는 sampler
- span/log를 바로 보낼지 batch로 묶을지 결정하는 processor
- metric measurement를 어떤 stream과 aggregation으로 만들지 결정하는 metric reader/view
- 데이터를 어디로 보낼지 결정하는 exporter
- service.name, deployment.environment 같은 resource 정보
- 종료 시 남은 데이터를 flush하는 shutdown path

이 구조에서 중요한 원칙은 라이브러리는 가능하면 API만 의존하고, 실제 SDK 설정은 애플리케이션 소유자가 결정해야 한다는 점이다. 라이브러리가 자체적으로 SDK를 초기화해버리면 서비스의 sampling, exporter, resource 정책을 침범할 수 있다.

---

## 4. Trace SDK에서 중요하게 본 부분

Trace SDK에서는 span이 만들어진 뒤 backend까지 가기 전에 여러 단계를 거친다.

```text
Span 생성
→ Sampler
→ SpanProcessor
→ Queue / Batch
→ Exporter
→ Collector 또는 Backend
```

### 4-1. Head sampling의 한계

Head sampling은 요청이 시작되는 시점에 이 trace를 남길지 말지 결정한다. 빠르고 비용이 낮지만, 요청이 나중에 성공할지 실패할지, p99 latency가 될지 알 수 없다.

예를 들어 “에러가 난 요청은 100% 보고 싶다”는 요구가 있을 때 head sampling만으로는 충분하지 않다. 요청 시작 시점에는 그 요청이 에러로 끝날지 모르기 때문이다.

이 문제를 해결하기 위해 tail sampling을 사용할 수 있다. Tail sampling은 trace가 끝난 뒤, 또는 일정 시간 span을 모은 뒤에 보존 여부를 결정한다. 예를 들어 에러 trace, 1초 이상 걸린 trace, 특정 route의 trace를 우선 보존하는 정책을 만들 수 있다.

하지만 tail sampling은 공짜가 아니다. 결정을 뒤로 미루는 동안 trace 데이터를 메모리에 들고 있어야 하므로 collector의 메모리 사용량과 지연이 증가한다. 즉 tail sampling은 에러 trace를 잘 보존하는 기능이면서 동시에 collector에 부담을 주는 기능이다.

### 4-2. BatchSpanProcessor와 shutdown flush

운영 환경에서는 보통 SimpleSpanProcessor보다 BatchSpanProcessor가 기본값에 가깝다. 매 span을 즉시 export하면 요청 처리 latency에 영향을 줄 수 있기 때문이다.

하지만 batch 방식은 queue와 flush 문제를 가진다. 애플리케이션이 종료될 때 남아 있는 span을 forceFlush하지 않으면 마지막 순간의 중요한 trace가 사라질 수 있다. 특히 장애 직전이나 프로세스 종료 직전에 생성된 데이터가 가장 먼저 유실될 수 있다는 점이 위험하다.

그래서 SDK 설정을 볼 때는 단순히 exporter가 붙어 있는지만 볼 것이 아니라 다음을 함께 확인해야 한다.

- batch queue size
- max export batch size
- exporter timeout
- retry policy
- shutdown / forceFlush 경로
- sampling policy

---

## 5. Context propagation과 baggage

Trace에서 중요한 것은 span object 자체보다 context propagation이다.

분산 시스템에서는 하나의 요청이 여러 서비스를 지나간다. 이때 traceparent, tracestate 같은 표준 header를 통해 trace context가 전파되어야 전체 요청 흐름이 하나로 이어진다.

또한 batch, fan-in, fan-out 구조에서는 parent-child 관계만으로 요청 흐름을 표현하기 어려울 수 있다. 여러 메시지를 한 번에 처리하는 Kafka consumer 같은 경우 producer span 하나를 parent로 잡기보다 span link를 사용하는 것이 더 정확할 수 있다.

### baggage의 위험성

Baggage는 여러 서비스로 context를 전파할 수 있는 기능이다. 편리하지만 잘못 쓰면 분산 PII 유출 통로가 될 수 있다.

예를 들어 baggage나 span attribute에 다음 값이 들어가면 여러 서비스와 telemetry backend로 복제될 수 있다.

- user email
- account id
- authorization header
- token
- query string
- 실험군이나 plan 정보

OpenTelemetry는 데이터를 잘 전파한다. 그래서 잘못된 데이터도 잘 전파한다. 운영 환경에서는 baggage key allowlist, 민감 header 제거, query string 제거, 외부 SaaS export destination 제한 같은 정책이 필요하다.

---

## 6. Metrics SDK와 cardinality

Metric은 trace와 데이터 모델이 다르다. Trace attribute는 개별 요청에 붙는 정보에 가깝지만, metric label은 시계열의 차원을 만든다.

예를 들어 HTTP latency metric에 다음 정도의 label이 붙는 것은 비교적 안전하다.

```text
method="GET"
route="/users/:id"
status_code="200"
```

하지만 다음과 같은 값을 label로 넣으면 문제가 된다.

```text
url="/users/123?token=..."
user_id="123"
request_id="abc"
session_id="xyz"
```

이 값들은 거의 무한히 늘어날 수 있다. metric label value가 늘어나면 새로운 time series가 만들어지고, backend의 저장 비용과 query 비용이 급격히 증가한다.

간단히 보면 service 10개, endpoint 50개, status code 5개, method 3개만 있어도 7,500개 series가 된다. 여기에 user_id 100만 개가 label로 붙으면 75억 개 series가 될 수 있다.

그래서 metric label은 metadata가 아니라 schema처럼 봐야 한다. 누구나 아무 attribute나 metric label로 올릴 수 있게 하면 안 되고, 다음과 같은 기준이 필요하다.

- raw URL 대신 template route 사용
- user_id, request_id, session_id label 금지
- service별 series 수 모니터링
- collector에서 label drop/relabel 적용
- cardinality budget 관리

---

## 7. Logs SDK에 대해 이해한 점

OpenTelemetry Logs는 단순히 stdout을 대체하는 개념이 아니다.

로그에 trace_id를 심으면 trace와 log를 어느 정도 연결할 수는 있다. 하지만 OTel Logs 모델은 그보다 더 넓다. Resource, severity, attributes, instrumentation scope, processor, exporter가 함께 포함된다.

즉 “로그에 trace_id만 넣었다”는 것은 OTel Logs를 사용하는 것과 같지 않다. trace_id는 상관관계의 일부일 뿐이고, 로그 자체를 어떤 resource와 scope에서 발생한 structured event로 다룰지까지 포함해야 OTel Logs 모델에 가까워진다.

---

## 8. Resource와 Semantic Convention

Resource는 telemetry를 만든 주체를 설명한다. 예를 들어 다음 값들이 여기에 해당한다.

- service.name
- service.version
- deployment.environment
- service.instance.id

이 정보가 없으면 backend에서 “어느 서비스의 어떤 환경에서 나온 데이터인지”를 구분하기 어렵다.

Semantic Convention은 단순히 필드명 취향을 맞추는 문제가 아니다. 여러 언어와 라이브러리, backend가 같은 의미를 같은 이름으로 이해하기 위한 계약이다. 예를 들어 HTTP 요청 duration, DB query, messaging operation 같은 항목이 서로 다른 이름으로 들어오면 dashboard와 alert를 공통으로 만들기 어렵다.

결국 Resource와 Semantic Convention은 관측 데이터의 쿼리 가능성과 상관분석 가능성을 결정한다.

---

## 9. Collector는 완충 계층이자 또 다른 장애 지점

OTel Collector는 애플리케이션 밖에서 telemetry를 받아 처리하는 pipeline이다. SDK와 Collector를 동일시하면 안 된다.

Collector는 다음 역할을 할 수 있다.

- backend exporter 설정 중앙화
- attribute filter / transform
- 여러 backend로 routing
- retry / queue
- tail sampling
- memory limiting

이런 점에서 Collector는 유용한 완충 계층이다. 하지만 잘못 설계하면 여러 서비스의 telemetry가 동시에 멈추는 shared dependency가 될 수도 있다.

Collector 배치 방식도 선택이 필요하다.

| 방식 | 장점 | 단점 |
|---|---|---|
| 앱에서 backend로 직접 전송 | 단순함 | backend 장애가 앱에 가까워짐 |
| Sidecar Collector | 앱별 격리 좋음 | pod마다 collector가 떠서 비용 증가 |
| DaemonSet Collector | 노드 단위로 효율적 | 서비스별 정책 분리가 어려울 수 있음 |
| Gateway Collector | 중앙 정책 관리 좋음 | 잘못 설계하면 SPOF |

중요한 관점은 Collector가 reliability를 자동으로 높여주는 장치가 아니라, reliability를 설계할 수 있게 해주는 제어면이라는 점이다.

---

## 10. Observability pipeline의 유실 지점

장애 상황에서 trace가 없다고 해서 요청이 없었다고 볼 수 없다. Telemetry는 여러 지점에서 사라질 수 있다.

가능한 유실 지점은 다음과 같다.

1. Head sampling에서 제외됨
2. SDK queue overflow 발생
3. 애플리케이션 종료 시 shutdown flush 누락
4. Collector memory limiter가 drop 또는 refuse
5. Exporter timeout 또는 retry 실패
6. Backend ingest quota 초과
7. Backend에는 들어갔지만 query/index delay 발생

그래서 장애 분석에서 질문은 “데이터가 있나?”가 아니라 “데이터가 어디까지 도착했나?”가 되어야 한다.

Dashboard에서 요청량이 줄어든 것처럼 보여도 실제 요청량이 줄어든 것이 아니라 metric pipeline이 막힌 것일 수 있다. 에러 trace가 안 보여도 에러가 없었던 것이 아니라 sampling에서 빠졌을 수 있다. 로그가 줄어든 것도 문제가 해결된 것이 아니라 log pipeline이 drop을 시작한 것일 수 있다.

---

## 11. Alert도 pipeline의 산출물이다

Alert는 metric을 기반으로 하지만, 실제로는 telemetry pipeline 전체의 마지막 산출물이다.

```text
record
→ aggregate
→ export interval
→ collector queue
→ backend ingest
→ query
→ evaluation interval
→ for-duration
→ alert
```

따라서 p95 latency alert가 5분 늦게 울렸다면 애플리케이션이 늦게 느려진 것일 수도 있지만, telemetry pipeline이나 alert evaluation 지연 때문일 수도 있다.

Alert latency를 해석할 때는 다음을 함께 봐야 한다.

- metric export interval
- collector queue 상태
- backend ingest delay
- query evaluation interval
- for-duration 설정
- dashboard/query cache

이 관점이 없으면 alert가 늦게 울렸을 때 애플리케이션 문제와 관측 pipeline 문제를 구분하기 어렵다.

---

## 12. Collector 자체도 관측해야 한다

애플리케이션을 관측하는 시스템도 관측 대상이어야 한다.

Collector를 production에서 사용한다면 최소한 다음 지표를 봐야 한다.

- receiver가 받은 span / metric / log 수
- refused span / metric / log 수
- exporter send failed 수
- dropped data 수
- queue size
- retry count
- memory limiter drop 수
- collector CPU / memory
- backend export latency
- telemetry freshness

가장 위험한 상황은 서비스 장애와 동시에 telemetry pipeline도 과부하로 drop을 시작하는데, 그 사실을 모르는 것이다. 이 경우 dashboard가 조용해 보일 수 있고, 실제 장애를 과소평가할 수 있다.

---

## 13. Observability를 위한 시스템에도 SLO가 필요하다

Observability를 보장하기 위한 시스템을 운영 대상으로 본다면, 관측 시스템 자체에도 SLO가 필요하다.

예를 들어 다음과 같은 기준을 둘 수 있다.

```text
Metric freshness:
  99% of metric points are queryable within 60 seconds.

Trace pipeline:
  collector-side drop rate < 1% over 5 minutes.

Alert latency:
  critical alerts fire within 2 minutes after condition is met.

Collector availability:
  gateway collector success rate > 99.9%.
```

이런 기준이 없으면 장애 때마다 “trace가 왜 없지?”, “dashboard가 왜 늦지?”, “alert가 원래 이렇게 늦나?”를 감으로 판단하게 된다.

관측 시스템도 사용자 서비스만큼은 아니더라도 명확한 기대치가 있어야 한다. 그렇지 않으면 “서비스가 정상이라서 조용한 것인지”, “관측 시스템이 망가져서 조용한 것인지” 구분하기 어렵다.

---

## 14. 운영 전 체크리스트

이번 내용을 바탕으로 OpenTelemetry를 production에서 사용하기 전 확인할 항목을 정리하면 다음과 같다.

### SDK 설정

- Batch queue size가 적절한가?
- Exporter timeout이 너무 길지 않은가?
- Retry policy가 있는가?
- Shutdown 시 forceFlush가 호출되는가?
- Sampling policy가 의도적으로 설정되어 있는가?

### Collector 설정

- Memory limiter가 있는가?
- Batch processor가 있는가?
- Sending queue가 있는가?
- Exporter 실패 시 retry/drop 정책이 명확한가?
- Collector 자체 dashboard와 alert가 있는가?

### Metric cardinality

- Raw URL을 label로 쓰고 있지 않은가?
- user_id, request_id, session_id가 label에 들어가지 않는가?
- service별 series 수를 보고 있는가?
- label allowlist 또는 drop rule이 있는가?

### Security / PII

- Authorization header가 attribute로 나가지 않는가?
- query string을 제거하는가?
- baggage key를 제한하는가?
- 외부 SaaS로 나가는 telemetry에 민감정보가 없는가?

### Alert latency

- metric export interval이 적절한가?
- backend ingest delay를 알고 있는가?
- alert evaluation interval과 for-duration을 이해하고 있는가?

---

## 15. 내 생각

이번 내용을 정리하면서 가장 크게 느낀 것은, Observability는 단순히 도구를 붙인다고 보장되지 않는다는 점이다.

이전에는 “trace를 잘 남기면 장애 분석이 쉬워진다” 정도로 생각했다. 하지만 실제로는 trace를 남기는 것만큼이나, 그 trace가 어떤 pipeline을 지나 backend까지 도착하는지, 그 과정에서 무엇이 사라지고 지연될 수 있는지를 이해하는 것이 중요했다.

Observability는 특정 표준이나 도구를 도입한다고 자동으로 좋아지는 것이 아니다. 오히려 관측 가능성을 보장하기 위한 새로운 시스템을 하나 더 운영하게 되는 것에 가깝다. SDK queue, exporter, collector, backend ingest, query, alert evaluation까지 모두 장애 지점이 될 수 있다.

그래서 운영 관점에서 중요한 질문은 다음이라고 생각한다.

> 내가 보고 있는 데이터는 어떤 과정을 거쳐 여기까지 왔고, 그 과정에서 무엇이 사라졌는가?

그리고 한 단계 더 나아가면 이런 질문도 필요하다.

> 이 데이터를 운반하는 telemetry pipeline은 장애 상황에서도 충분히 견고한가?

결국 Observability를 보장하려면 애플리케이션만 잘 계측하는 것으로는 부족하다. 데이터를 수집하고, 버퍼링하고, 샘플링하고, 전송하고, 저장하고, 조회하고, alert로 바꾸는 전체 시스템이 일정 수준 이상으로 안정적이어야 한다. 내가 이번에 더 크게 느낀 부분은 “OpenTelemetry를 잘 쓰자”가 아니라, “Observability 자체를 하나의 신뢰성 있는 시스템으로 운영해야 한다”는 점이다.

---

## 16. 참고 자료

- OpenTelemetry 공식 문서: https://opentelemetry.io/docs/
- OpenTelemetry Specification: https://opentelemetry.io/docs/specs/otel/
- OpenTelemetry Specification GitHub: https://github.com/open-telemetry/opentelemetry-specification
- W3C Trace Context: https://www.w3.org/TR/trace-context/
