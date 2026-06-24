# Week 02 - Monitoring & Observability

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 2주차 |
| 주제 | Monitoring과 Observability 개념 이해 |
| 일자 | 2026-05-14 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 박시윤, 구혜준, 우다현, 이장원, 김태영, 유지선, 이유성, 윤서영, 박은서, 이서영, 신웅비, 이채은 |
| 결석 | 없음 |

---

## 2. 이번 주 학습 범위

- Monitoring과 Observability의 차이
- Metrics, Logs, Traces의 역할
- SLI, SLO, SLA
- Google Golden Signals
- Prometheus, Grafana, OpenTelemetry, APM 도구의 역할
- Trace, span, exemplar, service monitor 등 주요 용어

---

## 3. 발표자

| 순서 | 이름 | 발표 주제 |
|---|---|---|
| 1 | 신웅비 | Golden Signals와 실무 모니터링 경험 |
| 2 | 박은서 | Metrics, Logs, Traces와 Observability 기본 개념 |
| 3 | 이서영 | Monitoring, Observability, SLI/SLO, Prometheus/OpenTelemetry |
| 4 | 유지선 | LY Tech Blog 기반 SLI/SLO와 error budget |
| 5 | 이유성 | 하이브리드 클라우드 면접 과제와 모니터링 설계 경험 |

---

## 4. 발표별 주요 내용

### 신웅비

- Google Golden Signals를 latency, traffic, errors, saturation으로 정리
- 평균 응답 시간보다 P95/P99 latency가 사용자 경험과 장애 전조를 더 잘 보여줄 수 있다는 점 공유
- 반복 alert가 사람을 무감각하게 만드는 alert fatigue 문제 공유
- Grafana, Tempo, Mimir, Loki, Pyroscope 기반 실무 관찰 경험 공유

### 박은서

- Observability를 시스템 내부 상태와 원인을 이해하기 위한 운영 방식으로 정리
- Metrics는 수치 기반 상태, Logs는 사건 기록, Traces는 요청 흐름으로 구분
- 세 데이터를 따로 보는 것보다 상관관계로 연결하는 과정이 어렵고 중요하다는 점 공유

### 이서영

- Monitoring, Observability, Visibility 차이를 개념적으로 비교
- SLI/SLO, Prometheus pull 방식, ServiceMonitor, Exemplar 등을 추가 조사
- OpenTelemetry가 Metrics/Logs/Traces를 모두 다룰 때 Prometheus가 어떤 역할을 계속 가지는지 질문 제기

### 유지선

- Critical User Journey를 먼저 잡고 사용자 관점의 SLI/SLO를 설계하는 방식 소개
- 99.9, 99.99, 99.999 목표가 장애 허용 시간과 자동화 수준을 바꾸는 점 정리
- Error budget을 개발팀과 운영팀이 배포 속도와 안정성 사이에서 합의하는 기준으로 설명

### 이유성

- 하이브리드 클라우드 아키텍처 면접 과제에서 DR과 모니터링을 함께 설명한 경험 공유
- 도구 이름보다 수집 대상, 대시보드 구성, alert 기준, drill-down workflow를 구체화해야 한다는 피드백 정리

---

## 5. 공통으로 나온 질문

- APM과 Observability는 어디까지 같은 개념으로 볼 수 있는가?
- OpenTelemetry가 표준 수집 체계라면 Prometheus는 어떤 강점을 유지하는가?
- Visibility를 설명할 때 어떤 데이터와 대시보드 흐름까지 말해야 충분한가?
- Active-active DB 구성은 실제 운영에서 어느 정도 현실적인가?

---

## 6. 운영 관점 인사이트

- Observability는 도구 이름보다 데이터 수집, 연결, 해석 흐름을 설명하는 것이 중요
- SLI/SLO는 기술 지표이면서 동시에 개발팀과 운영팀의 합의 언어
- 좋은 alert는 실제 action을 요구해야 하며, 반복 수동 조치가 필요하면 자동화나 기준 조정 검토
- Trace와 log drill-down은 장애 원인을 빠르게 좁히는 데 유용
- 면접이나 설계 설명에서는 지표, 수집 경로, dashboard, alert 기준을 함께 설명하는 것이 설득력 있음

---

## 7. 다음 주 과제

- 교재 Chapter 2 범위 학습
- `members/{영문이름}/week03.md`에 과제 정리
- APM과 Observability, Prometheus와 OpenTelemetry의 역할 차이 추가 고민
- 실제 운영/프로젝트에서 어떤 지표를 먼저 볼지 질문 정리
