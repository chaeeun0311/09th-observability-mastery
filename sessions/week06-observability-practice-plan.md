# Week 06 - Observability Practice Plan

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 6주차 |
| 주제 | Observability 실습 주제 선정 |
| 일자 | 2026-06-11 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 박시윤, 구혜준, 우다현, 이장원, 김태영, 유지선, 이유성(면접), 윤서영, 신웅비 |
| 결석 | 박은서, 이서영, 이채은 |

---

## 2. 이번 주 학습 범위

- Metrics, Logs, Traces 상관관계
- Exemplar, span metrics, trace ID
- OpenTelemetry agent와 instrumentation
- Base/Project 실습 방향 선정
- 다음 주 실습 공유 준비

---

## 3. 실습 방향

| 구분 | 방향 |
|---|---|
| Base | 책 예제나 demo repository를 기반으로 Prometheus, Grafana, Loki, Tempo, OpenTelemetry를 직접 구성 |
| Project | 개인 프로젝트, 졸업 프로젝트, 홈서버, 운영 중인 서비스에 Observability 적용 |

---

## 4. 참여자별 계획

| 이름 | 계획 |
|---|---|
| 김태영 | Prometheus/Grafana 기본 데모를 통해 실제 프로젝트에 적용할 모니터링 구성 탐색 |
| 유지선 | 홈서버 기반 Spring 서비스에 OpenTelemetry, Loki, Grafana를 붙여 병목과 오류 관측 |
| 박준우 | 홈서버와 개인 agent stack에 monitoring과 alerting 적용 |
| 신웅비 | OpenTelemetry SDK와 auto instrumentation 내부 동작 분석 |
| 이장원 | Kubernetes 기반 online judge 서비스의 resource limit, HPA 기준, dashboard 설계 |
| 구혜준 | 졸업 프로젝트 microservices에 Metrics/Logs/Traces, SLI/SLO, Alertmanager 적용 |
| 박시윤 | Python 기반 OpenTelemetry demo 실습 |
| 우다현 | Grafana/Prometheus와 cloud metrics dashboard 방향 구체화 |
| 이서영 | TNS 예제 기반 Loki/Tempo/Prometheus 실습과 custom dashboard 구성 |

---

## 5. 주요 논의 내용

### Metrics, Logs, Traces 연결

- Metrics에서 Traces로 넘어갈 때 exemplar를 활용할 수 있음
- Trace에서 metric을 만들 때 span metrics 개념을 사용할 수 있음
- Logs와 Traces는 trace ID를 통해 같은 요청 흐름으로 연결 가능
- Metrics와 Logs는 표준 연결 방식이 약하므로 label, timestamp, naming 규칙 설계 필요

### 실습 대상 선정

- 홈서버나 개인 프로젝트도 좋은 실습 대상이 될 수 있음
- 실제 사용자가 적더라도 느린 구간, 간헐적 오류, 외부 API 호출, model inference latency 같은 관측 포인트를 만들 수 있음
- 졸업 프로젝트나 online judge처럼 여러 서비스가 연결된 프로젝트는 SLI/SLO와 alert 설계까지 붙여 보기 좋음

---

## 6. 운영 관점 인사이트

- 실습은 도구를 모두 설치하는 것이 아니라 관측하고 싶은 질문을 먼저 정해야 함
- OpenTelemetry는 collector 실행뿐 아니라 SDK와 instrumentation이 client library를 어떻게 감싸는지 이해할 수 있는 좋은 학습 대상
- Project 방향은 실제 프로젝트 구조를 설명하고 어떤 지표로 어떤 판단을 할지 정리하는 것이 중요
- 다음 세션은 읽은 내용을 설명하는 자리보다 실제로 해 본 결과, 막힌 점, 알게 된 점을 공유하는 자리로 운영

---

## 7. 다음 주 과제

- 각자 선택한 Base 또는 Project 실습 진행
- 새로 알게 된 점, 막힌 점, 다음에 확인할 점 정리
- dashboard, trace, log, alert 등 화면이나 결과물을 공유할 수 있게 준비
