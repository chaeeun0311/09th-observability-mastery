# Week 04 - Prometheus & Kubernetes Monitoring

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 4주차 |
| 주제 | Prometheus와 Kubernetes 모니터링 |
| 일자 | 2026-05-28 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 박시윤, 우다현, 유지선(면접), 이유성, 윤서영, 박은서, 이서영 |
| 결석 | 구혜준, 이장원, 김태영, 신웅비, 이채은 |

---

## 2. 이번 주 학습 범위

- Prometheus 기본 구조
- Exporter와 scrape 방식
- Prometheus Operator, ServiceMonitor, PodMonitor
- Prometheus Adapter와 HPA 연동
- Metrics Server와 custom metrics 차이
- TSDB, WAL, block, cardinality

---

## 3. 주요 공유 내용

### Prometheus 기본 흐름

- Exporter는 애플리케이션이나 인프라의 metric을 `/metrics` endpoint로 노출
- Prometheus server는 pull 방식으로 scrape하고 TSDB에 저장
- 운영자는 PromQL과 dashboard를 통해 metric을 조회하고 alert rule을 설정

### Kubernetes 연동

- Prometheus Operator는 Prometheus, Alertmanager, ServiceMonitor, PodMonitor 운영을 자동화하는 controller
- ServiceMonitor와 PodMonitor는 Kubernetes 내부 scrape 대상을 선언하는 리소스
- Prometheus Adapter는 Prometheus metric을 Kubernetes Metrics API로 변환해 HPA가 사용할 수 있게 함
- Metrics Server만 쓰면 CPU/Memory 중심이고, Prometheus를 붙이면 HTTP 요청 수, queue 길이 등 custom metrics 활용 가능

### 저장 구조와 확장성

- Prometheus TSDB는 sample, chunk, block 구조로 데이터를 저장
- 최신 데이터는 memory head에 있고 장애 복구를 위해 WAL에 먼저 기록
- Cardinality가 높아지면 저장량과 query 비용이 급격히 커질 수 있음
- 장기 저장과 고가용성은 Thanos, Mimir 같은 확장 구성에서 다시 다룰 수 있음

---

## 4. 공통으로 나온 질문

- 외부 VM, DB, queue, Redis, Kafka 같은 리소스는 어떻게 모니터링하는가?
- Node Exporter와 서비스별 Exporter는 어떤 차이가 있는가?
- Prometheus Operator와 Helm은 어떤 역할 차이가 있는가?
- KEDA와 HPA는 어떤 상황에서 구분해 쓰는가?

---

## 5. 운영 관점 인사이트

- Prometheus는 설치 자체보다 scrape 대상과 metric 설계가 중요
- Kubernetes 기본 metric만으로는 서비스 상태를 충분히 설명하기 어려움
- 실제 운영 현장에서는 사내 플랫폼이나 SaaS를 사용하는 경우도 많고, 운영자는 알람 해석과 장애 대응 절차에 더 집중할 수 있음
- Cardinality는 초기에는 잘 보이지 않지만 규모가 커질수록 비용과 성능에 큰 영향을 주는 설계 요소

---

## 6. 다음 주 과제

- Prometheus 핵심 흐름 복습
- Cardinality, Thanos, Mimir 등 확장 주제 추가 조사
- PR 미제출자는 제출 또는 진행 상태 공유
- 마지막 주 오프라인/회식 참석 가능 여부 확인
