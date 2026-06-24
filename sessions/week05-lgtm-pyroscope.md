# Week 05 - LGTM Stack & Pyroscope

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 5주차 |
| 주제 | LGTM Stack과 Pyroscope 운영 경험 |
| 일자 | 2026-06-04 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 구혜준, 우다현, 김태영, 유지선, 이유성, 이서영, 신웅비, 이채은 |
| 결석 | 박시윤, 이장원, 윤서영, 박은서 |

---

## 2. 이번 주 학습 범위

- Grafana LGTM Stack
- Loki, Grafana, Tempo, Mimir 역할
- Pyroscope와 continuous profiling
- Metrics, Logs, Traces, Profiling의 차이
- 실무 장애 대응에서 dashboard와 trace를 연결하는 방식

---

## 3. 발표자 및 공유자

| 이름 | 공유 내용 |
|---|---|
| 이서영 | Tempo, Jaeger, Loki, Mimir 개념 정리 |
| 신웅비 | Pyroscope, continuous profiling, flame graph |
| 구혜준 | LGTM Stack과 운영 환경의 장애 대응 흐름 |
| 유지선 | 면접 경험 공유 |
| 이유성 | 네트워크 직무 면접 경험 공유 |

---

## 4. 발표별 주요 내용

### LGTM Stack

- Loki는 log를 label 중심으로 조회하고 Grafana와 함께 log 탐색을 지원
- Mimir는 Prometheus metric의 장기 저장, 고가용성, 대규모 확장을 보완
- Tempo와 Jaeger는 distributed tracing 도구이며 trace 저장과 분석에 사용
- Grafana는 metric, log, trace를 한 화면에서 연결해 보는 중심 도구 역할

### Pyroscope와 Profiling

- Pyroscope는 CPU/Memory 사용을 함수 또는 code line 수준으로 좁혀 보는 continuous profiling 도구
- Metrics, Logs, Traces가 증상과 위치를 좁힌다면 profiling은 어떤 코드가 비효율적인지 확인하는 데 유용
- eBPF 기반 수집과 SDK 기반 수집은 runtime 특성과 함수명 식별 가능성에 따라 선택이 달라질 수 있음
- Sampling 방식과 수집 주기를 조절하면 운영 서비스에서도 감당 가능한 overhead로 활용 가능

### 장애 대응 흐름

- Alert 확인 후 dashboard, metrics, Kubernetes event, logs, traces 순서로 원인을 좁히는 흐름 공유
- Custom metrics는 숫자로 보고 싶은 boundary를 직접 정의하고, 세부 흐름은 traces로 확인하는 방식이 적절
- 도구가 있어도 log coverage, 문서화, 책임 경계가 부족하면 troubleshooting 체계는 여전히 어려울 수 있음

---

## 5. 공통으로 나온 질문

- Loki, Mimir, Tempo는 Prometheus와 어떤 관계로 이해해야 하는가?
- Profiling은 Metrics/Logs/Traces와 어떤 문제를 다르게 해결하는가?
- eBPF와 SDK 기반 profiling은 언제 각각 적합한가?
- Continuous profiling을 항상 켜 두면 성능 부담은 어느 정도인가?

---

## 6. 운영 관점 인사이트

- LGTM Stack은 개별 도구 묶음이 아니라 Logs, Metrics, Traces를 연결해서 보는 운영 흐름
- Profiling은 장애 원인 분석을 코드 수준까지 내려가게 해 주는 보완 축
- SaaS APM은 편하지만 비용 부담이 커질 수 있어 자체 구축과 병행 전략을 고려할 수 있음
- 실무에서는 도구 도입보다 팀이 실제로 dashboard와 trace를 읽고 대응하는 습관을 만드는 것이 더 어려움

---

## 7. 다음 주 과제

- 졸업 프로젝트나 개인 프로젝트에 Metrics/Logs/Traces 기반 모니터링을 붙여 볼 대상 선정
- Grafana/LGTM 또는 OpenTelemetry 실습 범위 구체화
- 실습 주차에 Base 또는 Project 방향으로 진행할 계획 정리
