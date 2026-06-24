# Week 03 - MSA Resilience

## 세션 정보

| 항목 | 내용 |
|---|---|
| 주차 | 3주차 |
| 주제 | MSA 복원성과 운영 경험 토론 |
| 일자 | 2026-05-21 |
| 진행 시간 | 목요일 21:00 ~ 22:30 |
| 진행자 | 박준우 |

---

## 1. 참석 현황

| 구분 | 이름 |
|---|---|
| 출석 | 박준우, 구혜준, 우다현, 이장원, 김태영, 유지선, 이유성(면접), 윤서영, 박은서, 이서영, 신웅비, 이채은 |
| 결석 | 박시윤 |

---

## 2. 이번 주 학습 범위

- MSA와 분산 시스템의 운영 난이도
- SPOF, Load Balancer, Service Mesh, Istio
- HPA와 autoscaling 기준
- Resilience pattern
- SLI/SLO 기반 운영 프로세스
- Sharding, hash, time-series data 개념

---

## 3. 발표자 및 공유자

| 이름 | 공유 내용 |
|---|---|
| 이채은 | SPOF, Load Balancer, Service Mesh, HPA, resilience pattern |
| 우다현 | Load Balancer 유형, SLI/SLO, 장애 대응 flow |
| 박준우 | Chapter 2 핵심 요약, HPA와 관측성 데이터 흐름 |
| 구혜준 | 플랫폼/SRE 조직의 운영 경험과 autoscaling 사례 |
| 신웅비 | 운영 환경의 alert context와 장애 대응 경험 |

---

## 4. 발표별 주요 내용

### MSA와 복원성

- MSA 환경에서는 한 서비스 장애가 downstream service를 통해 전체 장애로 전파될 수 있음
- Retry, rate limit, bulkhead, circuit breaker, fallback은 장애 전파를 제한하기 위한 설계 패턴
- Service Mesh와 sidecar는 application code를 직접 바꾸지 않고 traffic control, security, telemetry를 붙이기 위한 방식

### Autoscaling과 HPA

- CPU 80% 같은 단순 기준만으로는 의미 있는 autoscaling을 설계하기 어려움
- 서비스별 traffic pattern, resource profile, 부하 테스트, custom metrics를 함께 고려해야 함
- Kubernetes Metrics Server는 CPU/Memory 중심이고, Prometheus Adapter나 KEDA를 붙이면 더 다양한 기준을 사용할 수 있음

### 운영 프로세스

- 장애 대응은 alert 확인에서 끝나지 않고 metrics, logs, traces, event, dashboard를 통해 원인 구간을 좁히는 과정
- SLI/SLO는 운영 목표와 장애 허용 범위를 명확히 하는 기준
- Alert fatigue를 줄이려면 알림 기준과 후속 action이 명확해야 함

---

## 5. 공통으로 나온 질문

- HPA threshold는 실제 운영에서 어떻게 잡아야 하는가?
- CPU/Memory 외에 어떤 custom metrics를 autoscaling 기준으로 쓸 수 있는가?
- Service Mesh와 eBPF/Cilium은 어느 수준부터 도입하는 것이 적절한가?
- SRE와 DevOps의 업무 경계는 실제 조직에서 어떻게 나뉘는가?

---

## 6. 운영 관점 인사이트

- Chapter 2는 세부 기술보다 분산 시스템 운영의 큰 지형도를 잡는 장으로 보는 것이 적절
- Autoscaling은 설정값보다 검증 과정이 중요하며, 부하 테스트와 실제 트래픽 특성을 함께 봐야 함
- SRE/DevOps 역할은 조직마다 다르고, ticket routing과 책임 경계가 모호해질 수 있음
- Alert 분석을 자동화하려면 알림 본문뿐 아니라 배포 이력, dashboard, log, runbook context까지 연결하는 것이 중요

---

## 7. 다음 주 과제

- 교재 Chapter 3 및 Prometheus 범위 학습
- `members/{영문이름}/week04.md`에 과제 정리
- 후반부 실습에서 Base 또는 Project 중 어떤 방향으로 갈지 고민
- 오프라인 북스터디 참석 가능 일정 응답
