# Week 4 - 책 범위 정리

## 0. 기본 정보

- 이름: 구혜준
- 주차: Week 4
- 읽은 범위:
  - Chapter 3. 관측 가능성의 시작, Prometheus, p.131-188
- 선택 유형:
  - [x] 책 범위 정리
  - [ ] 딥다이브 주제 정리

---

## 1. 이번 주 내용 한 줄 요약

이번 주에는 Prometheus를 중심으로 메트릭 수집, 시계열 데이터 저장, Grafana 시각화, 알림 구성, Kubernetes HPA 연계, Federation과 Thanos를 통한 확장 구조까지 학습하며 클라우드 네이티브 운영에서 관측 가능성이 어떻게 구성되는지 이해했다.

---

## 2. 책 내용 핵심 요약

1. Prometheus는 애플리케이션, 노드, 컨테이너 등에서 노출하는 메트릭을 주기적으로 수집하고, 이를 시계열 데이터베이스에 저장한다. 이후 PromQL을 통해 메트릭을 조회하거나 Grafana와 연동해 대시보드로 시각화할 수 있다.

2. Prometheus의 기본 운영 흐름은 메트릭 수집, 시계열 저장, 쿼리 및 시각화, 알림 규칙 평가, Alertmanager를 통한 통지로 이어진다. Kubernetes 환경에서는 service discovery를 통해 변경되는 Pod나 Service를 자동으로 탐지할 수 있어 동적인 클라우드 네이티브 환경에 적합하다.

3. Prometheus의 알림 기능은 rule manager와 Alertmanager를 통해 구현된다. Prometheus는 alerting rule을 평가해 조건이 만족되면 알림을 생성하고, Alertmanager는 이를 받아 Slack, Email 등 실제 통지 채널로 전달한다.

4. 알림 상태는 크게 inactive, pending, firing으로 나뉜다. inactive는 조건을 만족하지 않는 정상 상태이고, pending은 조건은 만족했지만 설정한 지속 시간에는 아직 도달하지 않은 상태이다. firing은 조건이 일정 시간 이상 지속되어 실제 알림이 발생한 상태를 의미한다.

5. Cardinality는 Prometheus 성능에 큰 영향을 준다. label 조합이 많아질수록 time series 수가 증가하기 때문에, user_id나 request_id처럼 값이 계속 달라지는 label은 피하는 것이 좋다. Cardinality를 줄이면 저장 공간과 메모리 사용량을 줄이고 쿼리 성능도 개선할 수 있다.

---

## 3. 중요하다고 생각한 개념

## 개념 1. Prometheus Operator, Exporter, Adapter

### 개념 설명

Prometheus Operator는 Kubernetes 환경에서 Prometheus와 Alertmanager를 더 쉽게 설치하고 관리할 수 있도록 도와주는 도구이다. Helm chart와 함께 사용하면 Prometheus 생태계를 비교적 쉽게 구성할 수 있다.

Prometheus Exporter는 특정 시스템의 메트릭을 Prometheus가 읽을 수 있는 형식으로 변환해 `/metrics` 엔드포인트에 노출하는 소프트웨어 또는 에이전트이다. 예를 들어 node-exporter는 서버의 CPU, memory, disk, network 같은 지표를 제공한다.

Prometheus Adapter는 Prometheus에 저장된 메트릭을 Kubernetes Custom Metrics API 형태로 노출해 HPA가 사용할 수 있도록 한다. 즉, Prometheus가 직접 Pod를 늘리는 것이 아니라, Adapter가 메트릭을 Kubernetes에 전달하고 HPA가 이를 기반으로 오토스케일링을 수행한다.

### 중요하다고 생각한 이유

Prometheus를 실제 Kubernetes 환경에서 운영하려면 단순히 메트릭을 수집하는 것뿐 아니라, Exporter, Operator, Adapter가 각각 어떤 역할을 하는지 이해해야 하기 때문이다.

### 운영 관점에서의 의미

이 구조를 이해하면 CPU나 memory 같은 기본 지표뿐 아니라 request count, latency, queue length 같은 서비스 지표를 기반으로도 오토스케일링을 구성할 수 있다. 따라서 단순 모니터링을 넘어 실제 운영 자동화와 연결될 수 있다는 점에서 중요하다.

---

## 개념 2. Prometheus Adapter의 4가지 규칙

### 개념 설명

Prometheus Adapter 설정에는 discovery, association, naming, querying 규칙이 있다.

Discovery는 Adapter가 어떤 Prometheus 메트릭을 찾을지 정하는 단계이다.

Association은 찾은 메트릭이 어떤 Kubernetes 리소스와 연결되는지 판단하는 단계이다.

Naming은 해당 메트릭을 Kubernetes Custom Metrics API에서 어떤 이름으로 노출할지 정하는 단계이다.

Querying은 HPA 등이 특정 메트릭 값을 요청했을 때 이를 어떤 PromQL 쿼리로 변환할지 정하는 단계이다.

### 중요하다고 생각한 이유

Custom metrics 기반 오토스케일링을 구현하려면 단순히 메트릭이 존재하는 것만으로는 부족하고, 그 메트릭이 어떤 리소스와 연결되는지 정확히 정의해야 하기 때문이다.

### 운영 관점에서의 의미

이 규칙을 잘못 설정하면 HPA가 원하는 메트릭을 찾지 못하거나 잘못된 값을 기준으로 스케일링할 수 있다. 따라서 실제 운영에서는 메트릭 이름, label, Kubernetes 리소스 매핑을 명확히 관리하는 것이 중요하다.

---

## 4. 이해가 어려웠던 부분

### 어려웠던 부분

- Federation 아키텍처
- 계층적 Federation과 교차 서비스 Federation의 차이
- Federation과 Sharding의 차이
- Thanos 아키텍처가 전체적으로 작동하는 방식

### 왜 어려웠는지

Federation은 여러 Prometheus 서버의 메트릭을 상위 Prometheus가 다시 수집하는 구조이고, Sharding은 수집 대상을 여러 Prometheus 인스턴스에 나누어 부하를 분산하는 구조이다. 둘 다 Prometheus 확장 방식이라는 점에서는 비슷해 보이지만, 목적이 다르기 때문에 한 번에 구분하기 어려웠다.

Thanos도 Prometheus의 한계를 보완하는 기술이라는 점은 이해했지만, Sidecar, Querier, Store Gateway, Object Storage, Compactor가 각각 어떤 역할을 하고 전체 요청 흐름이 어떻게 이어지는지는 아직 더 정리가 필요하다고 느꼈다.

---

## 5. 내 생각, 경험, 질문

Prometheus 기반의 메트릭 수집과 Grafana 시각화는 클라우드 네이티브 운영에서 가장 기본이 되는 구조라고 느꼈다. 특히 알림을 구성할 때 단순히 CPU 사용률이 높다거나 메모리가 부족하다는 식의 인프라 지표만 보는 것이 아니라, 실제 서비스 품질을 반영하는 SLO 지표를 기준으로 삼는 것이 중요하다고 생각했다.

다만 책에서는 SLO 기반 알림이 중요하다는 방향성은 제시되었지만, 실제로 어떤 지표를 SLI로 잡고 어느 정도 임계값을 설정해야 하는지는 더 구체적인 사례가 필요하다고 느꼈다. 예를 들어 웹 서비스라면 request latency, error rate, availability를 어떻게 조합해 알림을 만들지 궁금했다.

또한 실제 프로젝트에 적용한다면 가장 어려운 부분은 메트릭을 수집하는 것 자체보다, 너무 많은 알림이 발생하지 않도록 적절한 기준을 잡는 것이라고 생각했다. 잘못 설정된 알림은 오히려 운영자를 피로하게 만들 수 있기 때문에, 어떤 상황에서 warning을 주고 어떤 상황에서 critical alert를 발생시킬지에 대한 설계가 중요해 보인다.

---

## 6. 발표용 요약

### 발표 흐름

1. 이번 주에는 Prometheus, Grafana, Alertmanager, HPA 연계, Federation, Thanos를 중심으로 학습했다.
2. Prometheus는 메트릭을 수집하고 시계열 데이터로 저장하며, Grafana는 이를 시각화한다.
3. Alertmanager는 Prometheus의 알림을 실제 통지 채널로 전달하는 역할을 한다.
4. Kubernetes에서는 Prometheus Adapter를 통해 custom metrics를 HPA와 연결할 수 있다.
5. Federation과 Thanos는 Prometheus 단일 인스턴스의 한계를 보완하기 위한 확장 방식이다.
6. 아직 Federation과 Sharding의 차이, Thanos의 전체 동작 방식은 더 공부가 필요하다고 느꼈다.

### 발표 핵심 메시지

Prometheus는 단순한 모니터링 도구가 아니라, 메트릭 수집, 알림, 시각화, 오토스케일링, 장기 저장 구조와 연결되며 클라우드 네이티브 운영의 핵심 기반이 되는 도구이다.
