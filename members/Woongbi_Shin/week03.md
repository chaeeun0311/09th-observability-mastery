## 0. 기본 정보

- 이름: 신웅비
- 주차: 3주차
- 읽은 범위: Chapter 2.2 쿠버네티스 오토스케일링 (p.81 ~ p.95)
- 선택 유형:
    - [x]  책 범위 정리
    - [ ]  딥다이브 주제 정리

---

## 1. 이번 주 내용 한 줄 요약

> 오토스케일링은 "무엇을 늘릴 것인가(HPA/VPA/CA/KEDA)"와 "어떤 신호로 결정할 것인가(메트릭 선정)"라는 두 축으로 나뉜다. 도구는 메커니즘이고, 메트릭 선정이 정책이다.

---

## 2. 책 내용 핵심 요약

1. **HPA** — Pod 개수 조정. 공식: `desiredReplicas = ceil(currentReplicas × (currentMetric / targetMetric))`. 진동 방지용 stabilization window(기본 scale-down 300초)와 behavior policy(비대칭 설정 가능)가 있다.
2. **VPA** — Pod의 CPU/메모리 request·limit 조정. Off/Initial/Auto 세 모드. HPA와 같은 메트릭을 쓰면 충돌하므로 분리 필수.
3. **CA** — Pending pod 감지해 노드 추가/제거. HPA → CA 체인으로 분 단위 지연 발생. AWS에선 Karpenter가 ASG 우회하고 EC2 API 직접 호출하는 추세.
4. **KEDA** — 외부 이벤트 소스(SQS, Kafka, Redis Streams) 큐 길이 기반 스케일링. scale to zero 가능. 내부적으론 External Metrics API 노출하고 HPA가 실제 스케일 수행.
5. **메트릭 API 3종** — Resource Metrics API(CPU/메모리), Custom Metrics API(in-cluster 메트릭), External Metrics API(클러스터 밖 신호). HPA가 어느 API를 읽느냐가 동작 범위를 결정.
6. **Leading vs Lagging** — CPU/메모리는 lagging(부하의 결과), RPS·큐 깊이·동시 연결 수는 leading(부하의 원인). IO-bound 워크로드에선 CPU가 임계치까지 안 오르고 요청만 쌓이는 일이 흔해서 lagging만으로는 부족.

---

## 3. 중요하다고 생각한 개념

### 개념 1. HPA 알고리즘과 진동 방지

HPA 스케일링은 비율 계산 하나로 결정된다. 메트릭이 목표값을 넘으면 복제본을 늘리고, 미달이면 줄인다. 문제는 트래픽이 살짝만 오르내려도 Pod이 늘었다 줄었다 반복하는 진동(flapping)이 생긴다는 것.

이를 막기 위해 두 가지 장치가 있다.

- **stabilization window**: scale-down 시 기본 300초 대기. 임계치 이하라고 바로 줄이지 않는다.
- **behavior policy**: scale-up은 공격적으로(percent 100%), scale-down은 보수적으로(stabilizationWindowSeconds 600) — 이 비대칭 패턴이 표준.

지금까지 오토스케일링 = HPA에 CPU 임계값 설정이라고 생각했는데, "얼마나 빨리 늘릴 것인가"와 "얼마나 보수적으로 줄일 것인가"를 다르게 설정해야 한다는 게 핵심이었다. scale-up은 사용자 경험 보호를 위해 공격적으로, scale-down은 안정성과 비용을 위해 보수적으로. 특히 CA까지 거쳐야 하는 환경에선 scale-up 지연이 더 치명적이다.

---

### 개념 2. Leading vs Lagging Indicators

CPU와 메모리는 부하가 이미 발생한 뒤에 나타나는 **lagging** 신호다. 반면 RPS, 큐 깊이, 동시 연결 수는 부하의 원인에 가까운 **leading** 신호다. IO-bound 워크로드에선 CPU가 임계치까지 안 오르고 요청만 큐에 쌓이는 경우가 흔하다. 이럴 땐 CPU 기반 HPA가 요청 적체를 전혀 감지하지 못한다.

이 분리가 오토스케일링 설계의 핵심 질문을 바꿔놓는다. "어떤 메트릭을 기준으로 삼을 것인가?" — CPU 70%가 직관적이지만, 워크로드마다 적합한 메트릭이 다르다. API 서버는 RPS나 latency-p99, 큐 기반 워커는 큐 깊이가 더 나은 기준이다.

lagging만 쓰면 항상 한 발 늦는다. 사용자가 이미 느림을 느낀 뒤에 Pod이 늘어나는 구조. leading을 SLO와 직접 연결하면 부하가 쌓이기 전에 확장이 가능하지만, 노이즈에 더 민감하므로 stabilization window가 더 중요해진다.

---

### 개념 3. KEDA와 scale to zero

KEDA는 외부 이벤트 소스(SQS, Kafka, Redis Streams)의 큐 길이를 메트릭으로 써서 스케일링한다. HPA가 못 하는 **scale to zero**가 가능하다. 내부적으론 KEDA가 External Metrics API를 노출하고 HPA가 실제 스케일을 수행한다. 즉 KEDA는 HPA를 대체하는 게 아니라 보완하는 것.

EB + ASG + SQS + Lambda 조합을 k8s로 옮긴다고 가정하면, KEDA가 그 갭을 메워준다. Lambda의 scale-to-zero와 SQS 트리거를 k8s에서 재현하려면 KEDA 외엔 답이 없다. 또 KEDA가 내부적으로 HPA를 생성한다는 점에서, HPA가 모든 것의 중심이라는 걸 더 명확히 이해했다.

하지만 scale to zero는 cold start 문제가 있다. Pod이 0개에서 1개로 뜨는 시간이 비즈니스에 허용되는지 확인해야 하고, KEDA scaler의 폴링 인터벌이 반응 속도에 영향을 주므로 트래픽 패턴에 맞게 조정해야 한다.

---

## 4. 찾아본 내용 요약

V8과 JVM은 한 번 확보한 메모리를 OS에 거의 반납하지 않아, 프로세스 메모리가 GC 주기에 따라 톱니파 모양을 그린다. cgroup의 memory.usage_in_bytes는 RSS + page cache를 포함하고, OOM killer가 보는 값은 usage - inactive_file로 cAdvisor의 container_memory_working_set_bytes와 일치한다. 메모리 기반 HPA는 이 working_set을 신호로 쓰는데, V8/JVM 힙이 그대로 노출되어 부하가 아니라 GC 주기에 반응하게 된다. 따라서 메모리는 스케일 결정 신호가 아니라 건강성 신호로 분리해야 하며, 스케일은 RPS/큐 깊이/p95 latency로 결정하고 메모리는 증가율과 OOMKilled count로 모니터링하는 것이 올바른 접근이다.