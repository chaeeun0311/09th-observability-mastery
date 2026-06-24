# Week 07 - Observability Practice & LGTM Ops

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 7주차 |
| 주제 | Observability 실습 공유와 LGTM 운영 토론 |
| 일자 | 2026-06-18 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 박시윤, 구혜준, 이장원, 김태영, 유지선, 이유성, 윤서영, 박은서, 이서영, 신웅비, 이채은 |
| 결석 | 우다현 |
| 게스트/공유 | 장민호, 문영호 |

---

## 2. 이번 주 학습 범위

- 개인 실습 결과 공유
- 홈서버 health check와 host-level dashboard
- Spring Boot 서비스 OpenTelemetry agent 적용
- Kubernetes network failure diagnosis 프로젝트
- OpenTelemetry Operator와 Instrumentation resource
- LGTM/Tempo 운영 구조

---

## 3. 실습 공유

### 박준우

- 홈서버에 Uptime Kuma와 Netdata를 붙여 endpoint health check, host metric, hardware sensor, alerting 흐름 공유
- 개인 서버에서는 무거운 observability stack보다 실제로 볼 지표와 알림 목적을 먼저 정하는 방식이 현실적이라는 점 정리

### 유지선

- Spring Boot 기반 CRUD 서비스에 OpenTelemetry Java agent 적용
- JVM option 직접 주입 방식과 initContainer 기반 agent 주입 방식 비교
- Log에 trace ID, span ID, trace flag가 붙는 것까지 확인
- Loki/Grafana 연결은 추가 확인 과제로 남김

### 이서영/박은서

- Kubernetes 환경에서 네트워크 장애를 탐지하고 원인을 진단한 뒤 report를 생성하는 졸업 프로젝트 소개
- Prometheus 기본 metric이나 node exporter만으로 보기 어려운 TCP RTT, CWND 같은 지표를 eBPF agent로 수집하는 방향 공유
- Rule 기반 진단 결과와 근거를 사용자가 이해하기 쉬운 report로 정리하는 방향 논의

### 문영호

- OpenTelemetry Operator와 Instrumentation resource를 활용해 pod 생성 시점에 agent를 자동 주입하는 운영 방식 설명
- Argo CD application마다 agent 의존성을 넣는 방식보다 변경 전파와 장애 포인트를 줄일 수 있다는 관점 공유
- 개발자가 Grafana와 tracing을 실제로 쓰게 하려면 세미나와 가이드가 필요하다는 점 강조

### 장민호

- Alloy/OTLP 수집, Loki/Tempo/Mimir 전송, tenant 구분, Tempo metrics-generator, span metrics 등 LGTM 운영 구조 설명
- Sampling rate가 request count 계열 metric 신뢰도에 미치는 영향 공유
- Distributor, ingester, object storage, querier, consistent hashing, replication factor, OOM, query bottleneck 같은 실제 운영 지점 설명

---

## 4. 공통으로 나온 질문

- 개인 프로젝트에서 전체 observability stack을 다 붙이는 것이 항상 필요한가?
- OTel agent 주입은 JVM option, initContainer, Operator 중 어떤 방식이 적절한가?
- eBPF로 직접 수집해야 하는 metric은 node exporter metric과 어떻게 구분되는가?
- AI를 장애 진단 엔진으로 쓸지, 진단 결과를 정리하는 report 보조로 쓸지 어떻게 나눌 것인가?
- Tempo metrics-generator에서 sampling이 metric 신뢰도에 어떤 영향을 주는가?

---

## 5. 운영 관점 인사이트

- 작은 서비스나 홈서버에서는 가벼운 health check와 alerting부터 시작하는 것이 현실적
- Observability 도구를 설치해도 개발자가 query, trace, log를 읽을 수 있어야 운영 가치가 생김
- eBPF는 kernel/network 세부 지표를 얻기 위해 유용하지만, 어떤 진단 rule에 필요한 metric인지 설명할 수 있어야 함
- AI는 원인 진단을 완전히 맡기기보다 rule 기반 결과와 근거를 정리하는 보조 역할부터 잡는 것이 안전
- LGTM/Tempo 운영에서는 수집 경로, tenant 분리, sampling, 저장 구조, query 부하가 실제 장애 지점이 될 수 있음

---

## 6. 다음 주 과제

- 각자 실습 결과를 과제 파일에 정리
- Dashboard, report, trace, log, alert 등 보여줄 수 있는 산출물 준비
- OTel agent 주입 방식과 운영 적용 범위 추가 비교
- eBPF metric 수집 이유와 node exporter로 볼 수 있는 범위 재정리
- 외부 공유 시 회사/서비스/내부 운영 사례/인프라 구조 세부정보는 제외
