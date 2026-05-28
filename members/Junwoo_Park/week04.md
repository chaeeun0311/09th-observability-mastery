# Week 4 - Prometheus 개념 정리

## 0. 기본 정보

- 이름: 박준우
- 주차: 4주차
- 정리 범위: Prometheus 기본 구성, Prometheus Operator, Exporter, TSDB, Alertmanager, Sharding, Federation, Thanos
- 정리 방향: 이번 주도 긴 요약보다는 Prometheus를 운영할 때 자주 나오는 개념과 용어를 중심으로 정리했다.

---

## 1. 이번 주 전체 흐름

이번 주 내용은 Prometheus가 메트릭을 어떻게 수집하고, 저장하고, 조회하고, 알림과 오토스케일링에 연결하는지를 다룬다.

Prometheus는 단순히 메트릭을 보여주는 도구가 아니라, Kubernetes 환경에서 동적으로 바뀌는 대상들을 발견하고, exporter가 노출한 endpoint를 scrape하고, 수집한 시계열 데이터를 TSDB에 저장한 뒤 PromQL, alert rule, recording rule, HPA 연계 등에 활용한다.

크게 보면 이번 주 내용은 다음 흐름으로 이해했다.

1. Prometheus가 scrape 대상과 rule을 설정한다.
2. Exporter와 Kubernetes 리소스에서 메트릭을 Pull 방식으로 수집한다.
3. 수집한 sample을 메모리, WAL, block 구조를 통해 TSDB에 저장한다.
4. PromQL과 rule을 통해 조회, 사전 계산, 알림을 처리한다.
5. Prometheus Adapter를 통해 HPA와 custom metrics 기반 오토스케일링에 연결한다.
6. 규모가 커지면 sharding, federation, Thanos 같은 구조로 확장한다.

---

## 2. Prometheus 기본 구성

### Prometheus

- Prometheus: 메트릭을 Pull 방식으로 수집하고 시계열 데이터베이스에 저장해 조회, 알림, 오토스케일링 등에 활용하는 관측 가능성 도구

Prometheus는 메트릭 중심의 관측 가능성 도구다. 애플리케이션이나 exporter가 메트릭 endpoint를 노출하면 Prometheus Server가 주기적으로 가져와 저장한다.

### Prometheus Server

- Prometheus Server: exporter나 Kubernetes 리소스에서 메트릭을 스크래핑하고 TSDB에 저장하는 핵심 컴포넌트

Prometheus Server는 수집, 저장, 조회, rule 평가의 중심 역할을 한다. Prometheus를 운영한다고 할 때 가장 핵심이 되는 프로세스라고 볼 수 있다.

### Prometheus 설정 파일

- Prometheus 설정 파일: 스크래핑 대상, 규칙 파일, 알림 설정 등 Prometheus 동작 방식을 정의하는 구성 파일

설정 파일에는 어떤 대상을 얼마나 자주 scrape할지, 어떤 rule file을 읽을지, Alertmanager는 어디에 있는지 같은 정보가 들어간다.

### scrape config

- scrape config: Prometheus가 어떤 대상에서 어떤 주기로 메트릭을 수집할지 정의하는 설정

scrape config는 Prometheus 수집 범위를 결정한다. 수집 주기나 endpoint 설정이 잘못되면 메트릭이 누락되거나 불필요하게 많은 부하가 생길 수 있다.

### rule file

- rule file: recording rule과 alert rule처럼 Prometheus가 주기적으로 평가할 규칙을 정의하는 파일

rule file은 자주 사용하는 쿼리 결과를 미리 저장하거나, 특정 조건이 만족될 때 알림을 발생시키는 데 사용된다.

### PromQL

- PromQL: Prometheus에 저장된 시계열 데이터를 조회하고 계산하기 위한 쿼리 언어

PromQL은 Prometheus를 제대로 쓰기 위한 핵심이다. 단순 조회뿐 아니라 rate, sum, histogram 계산처럼 운영 지표를 해석하는 데 필요한 계산을 수행한다.

---

## 3. Prometheus Operator와 Kubernetes 서비스 디스커버리

### Prometheus Operator

- Prometheus Operator: Kubernetes 안에서 Prometheus 관련 자원을 관리하고 프로비저닝하는 오퍼레이터

Prometheus Operator를 사용하면 Prometheus 설정을 직접 파일로만 관리하지 않고, Kubernetes 커스텀 리소스를 통해 선언적으로 관리할 수 있다.

### Helm

- Helm: Kubernetes 애플리케이션을 패키지 형태로 설치하고 관리하는 도구

Prometheus, Grafana, Alertmanager 같은 구성 요소를 Kubernetes에 설치할 때 Helm chart를 자주 사용한다. 복잡한 YAML 구성을 패키지처럼 관리할 수 있다는 점이 장점이다.

### Operator

- Operator: Kubernetes 리소스의 생성, 변경, 운영 작업을 자동화하는 컨트롤러 패턴

Operator는 특정 애플리케이션 운영 지식을 컨트롤러로 구현한 방식이다. Prometheus Operator는 Prometheus 운영을 Kubernetes 방식으로 자동화한다.

### Kubernetes 서비스 디스커버리

- Kubernetes 서비스 디스커버리: Kubernetes 안에서 동적으로 증가하거나 감소하는 Service와 Pod를 자동으로 발견하는 기능

Kubernetes에서는 Pod가 계속 생성되고 삭제되므로 정적인 target 목록만으로는 운영이 어렵다. 서비스 디스커버리를 사용하면 변경되는 리소스를 자동으로 scrape 대상에 반영할 수 있다.

### ServiceMonitor

- ServiceMonitor: Prometheus Operator가 Service 기반 스크래핑 대상을 정의할 때 사용하는 커스텀 리소스

ServiceMonitor는 Kubernetes Service를 기준으로 scrape 대상을 정의한다. 일반적으로 애플리케이션이 Service를 통해 metric endpoint를 노출할 때 사용한다.

### PodMonitor

- PodMonitor: Prometheus Operator가 Pod 기반 스크래핑 대상을 정의할 때 사용하는 커스텀 리소스

PodMonitor는 Service가 아니라 Pod를 직접 기준으로 scrape 대상을 정의한다. Service를 만들기 애매한 Pod 단위 메트릭 수집에 사용할 수 있다.

### ServiceMonitorSpec

- ServiceMonitorSpec: 어떤 endpoint, port, interval, parameter로 스크래핑할지 정의하는 ServiceMonitor의 상세 설정

ServiceMonitorSpec에는 scrape 대상의 port, path, interval 같은 구체적인 설정이 들어간다. 실제로 Prometheus가 어떤 HTTP endpoint를 읽을지 결정하는 부분이다.

### Label

- Label: Prometheus 메트릭이나 Kubernetes 리소스를 구분하고 필터링하기 위한 키-값 쌍

Label은 Prometheus에서 매우 중요하다. 조회와 집계 기준이 되지만 label 조합이 너무 많아지면 high cardinality 문제가 생긴다.

### endpoint

- endpoint: exporter나 애플리케이션이 메트릭을 노출하는 HTTP 접근 지점

Prometheus는 endpoint에 HTTP 요청을 보내 메트릭을 가져온다. 보통 `/metrics` 경로를 사용하는 경우가 많다.

### Consul

- Consul: Kubernetes 외부 리소스의 서비스 디스커버리에 사용할 수 있는 도구

Kubernetes 내부에서는 Kubernetes 서비스 디스커버리를 쓰고, 외부 VM이나 다른 환경의 서비스는 Consul 같은 도구로 발견할 수 있다.

---

## 4. Exporter와 메트릭 수집

### Exporter

- Exporter: 특정 시스템이나 애플리케이션의 메트릭을 수집해 Prometheus가 읽을 수 있는 endpoint로 노출하는 에이전트

Exporter는 Prometheus가 이해할 수 있는 형식으로 메트릭을 노출한다. Prometheus는 exporter에 직접 요청해서 메트릭을 가져온다.

### Node Exporter

- Node Exporter: Unix 계열 커널, 하드웨어, OS 수준의 시스템 메트릭을 수집하는 공식 exporter

Node Exporter는 CPU, memory, disk, network 같은 노드 수준 메트릭을 수집할 때 사용한다. Kubernetes 노드나 VM 상태를 보기 위한 기본 구성에 가깝다.

### Custom Exporter

- Custom Exporter: 기본 exporter로 수집하기 어려운 애플리케이션 또는 MSA 메트릭을 노출하기 위해 직접 개발하는 exporter

비즈니스 지표나 특수한 시스템 메트릭은 직접 custom exporter를 만들어 노출할 수 있다. 다만 label 설계를 잘못하면 cardinality 문제가 생길 수 있다.

### Scraping

- Scraping: Prometheus Server가 Pull 방식으로 exporter의 endpoint에서 메트릭 데이터를 수집하는 과정

Prometheus는 scrape 주기에 따라 대상 endpoint를 호출한다. scrape interval이 너무 짧으면 부하가 커지고, 너무 길면 장애 감지가 늦어질 수 있다.

### Pull 방식

- Pull 방식: 수집 서버가 대상 endpoint에 직접 요청해 메트릭을 가져오는 방식

Pull 방식은 Prometheus가 수집 주기와 대상을 통제할 수 있다는 장점이 있다. 반대로 방화벽이나 네트워크 구조상 Prometheus가 대상에 접근할 수 있어야 한다.

---

## 5. Prometheus Adapter와 오토스케일링

### Prometheus Adapter

- Prometheus Adapter: Prometheus의 메트릭을 Kubernetes HPA가 사용할 수 있는 custom metrics API 형태로 변환하는 어댑터

Prometheus Adapter는 Prometheus와 Kubernetes HPA 사이를 연결한다. Prometheus에 저장된 메트릭을 HPA가 이해할 수 있는 API 형태로 바꿔준다.

### Metrics Server

- Metrics Server: Kubernetes에서 CPU, 메모리 같은 기본 리소스 메트릭을 제공하는 컴포넌트

Metrics Server는 기본 리소스 기반 HPA에 필요하다. CPU와 memory 기준으로 스케일링할 때 주로 사용된다.

### HPA

- HPA(Horizontal Pod Autoscaler): CPU, 메모리, custom metrics 등을 기준으로 Pod replica 수를 자동 조정하는 Kubernetes 기능

HPA는 부하에 따라 Pod 수를 늘리거나 줄인다. Prometheus Adapter와 연결하면 CPU, memory 외의 서비스 지표도 스케일링 기준으로 사용할 수 있다.

### Custom Metrics

- Custom Metrics: CPU와 메모리 외에 요청 수, 큐 길이, 비즈니스 지표처럼 서비스 특성을 반영한 사용자 정의 메트릭

Custom Metrics는 서비스의 실제 부하를 더 잘 표현할 때가 있다. 예를 들어 요청 수나 큐 길이가 CPU보다 더 빠르게 병목 신호를 보여줄 수 있다.

### KEDA

- KEDA(Kubernetes Event-driven Autoscaling): Prometheus 외에도 다양한 이벤트 소스를 기준으로 Kubernetes 워크로드를 확장하는 오토스케일링 도구

KEDA는 Prometheus뿐 아니라 메시지 큐, 이벤트 소스, 외부 시스템 지표를 기준으로 스케일링할 수 있다.

### Prometheus 오토스케일링 흐름

- Prometheus 오토스케일링 흐름: Prometheus Server가 수집한 메트릭을 Prometheus Adapter가 변환하고 HPA가 이를 기준으로 Pod 수를 조정하는 흐름

흐름으로 보면 `Exporter -> Prometheus Server -> Prometheus Adapter -> Custom Metrics API -> HPA -> Pod replica 조정` 순서로 이해할 수 있다.

---

## 6. Prometheus 라이프사이클

### 메트릭 수집과 시계열 저장

- 메트릭 수집과 시계열 저장: exporter에서 수집한 메트릭을 Prometheus TSDB에 시간 순서대로 저장하는 흐름

Prometheus의 기본 라이프사이클은 scrape한 sample을 시계열 데이터로 저장하는 것이다. 이 데이터가 이후 PromQL, 대시보드, 알림의 기반이 된다.

### 메트릭 측정과 리소스 오토스케일링

- 메트릭 측정과 리소스 오토스케일링: 수집된 메트릭을 기준으로 HPA나 KEDA가 리소스 확장 여부를 판단하는 흐름

메트릭은 관찰만을 위한 데이터가 아니라 운영 자동화의 입력값이 될 수 있다. 오토스케일링에서는 메트릭 품질이 곧 스케일링 품질에 영향을 준다.

### 자동 디스커버리

- 자동 디스커버리: 변경된 Service와 Pod를 자동으로 발견해 Prometheus 스크래핑 대상에 반영하는 과정

Kubernetes 환경에서는 리소스가 동적으로 변하기 때문에 자동 디스커버리가 중요하다. 새 Pod가 생겼는데 scrape 대상에 반영되지 않으면 메트릭이 비게 된다.

### HPA 연계

- HPA 연계: 트래픽 증가에 맞춰 늘어난 Pod로 요청이 분산되도록 오토스케일링과 로드밸런싱을 연결하는 과정

HPA가 Pod 수를 늘려도 트래픽이 새 Pod로 잘 분산되어야 의미가 있다. 그래서 오토스케일링은 서비스 디스커버리, 로드밸런싱, 메트릭 수집과 함께 봐야 한다.

---

## 7. Prometheus TSDB

### TSDB

- TSDB(Time Series Database): 시간 순서로 생성되는 메트릭 데이터를 저장하고 조회하는 시계열 데이터베이스

Prometheus는 내부 TSDB에 메트릭을 저장한다. 일반적인 관계형 데이터보다 시간 기준 조회와 집계에 초점이 맞춰져 있다.

### Time Series

- Time Series: 시간순으로 인덱싱되는 숫자 데이터 포인트의 시퀀스

Prometheus에서 하나의 metric 이름과 label 조합은 하나의 time series를 만든다. label 조합이 많아질수록 time series 개수도 늘어난다.

### Sample

- Sample: 특정 시점에 수집된 하나의 시계열 값

Sample은 timestamp와 value로 이루어진다. scrape할 때마다 새로운 sample이 생성된다.

### Chunk

- Chunk: Prometheus가 여러 sample을 묶어 저장하는 데이터 단위

Sample을 하나씩 따로 저장하면 비효율적이기 때문에 여러 sample을 chunk로 묶어 저장한다.

### Head Chunk

- Head Chunk: 새로 수집된 sample을 메모리에 먼저 기록하는 최신 chunk

최근 데이터는 head chunk에 먼저 쌓인다. 최신 쿼리를 빠르게 처리하기 위해 메모리를 적극적으로 사용한다.

### Block

- Block: 다수의 chunk, index, metadata를 묶어 디스크에 저장하는 TSDB의 불변 저장 단위

Prometheus는 일정 시간이 지나면 메모리의 데이터를 block 단위로 디스크에 저장한다. 한 번 생성된 block은 직접 수정하지 않는 불변 구조에 가깝다.

### Index

- Index: label과 시계열 데이터를 빠르게 찾기 위한 색인 구조

PromQL에서 label 조건으로 시계열을 찾을 때 index가 사용된다. label 설계가 쿼리 성능과 직접 연결된다.

### Metadata

- Metadata: block이나 metric에 대한 부가 정보

Metadata는 데이터 자체는 아니지만, block이나 metric을 해석하고 관리하는 데 필요한 정보를 담는다.

### Dataset

- Dataset: 여러 데이터 그룹을 묶어 부르는 데이터 집합

Prometheus 맥락에서는 여러 metric, label 조합, block을 포함하는 더 큰 데이터 묶음으로 이해할 수 있다.

### Data Point

- Data Point: 대시보드나 쿼리 결과에서 시계열로 출력되는 개별 데이터 값

Grafana 같은 도구에서는 PromQL 결과가 시간 축 위의 data point로 표시된다.

---

## 8. Cardinality와 메모리 관리

### Cardinality

- Cardinality: 특정 metric 이름과 label 조합으로 생성되는 시계열의 개수

Prometheus에서 cardinality는 매우 중요하다. label이 많거나 값 종류가 많으면 시계열 수가 빠르게 늘어난다.

### High Cardinality

- High Cardinality: label 조합이 너무 많아 시계열 수가 급격히 증가하는 상태

사용자 ID, request ID처럼 값이 거의 무한히 늘어나는 label을 붙이면 high cardinality가 발생할 수 있다.

### Cardinality Explosion

- Cardinality Explosion: 지나치게 많은 시계열이 생성되어 메모리, 저장소, 쿼리 성능에 부담을 주는 문제

Cardinality explosion은 Prometheus 운영에서 가장 조심해야 할 문제 중 하나다. 수집은 잘 되는 것처럼 보여도 메모리 사용량과 쿼리 비용이 급격히 커질 수 있다.

### LRU 알고리즘

- LRU 알고리즘: 가장 오랫동안 참조되지 않은 데이터를 먼저 교체하거나 내보내는 캐시 관리 기법

LRU는 제한된 메모리를 효율적으로 사용하기 위한 방식이다. 자주 쓰이지 않는 데이터를 먼저 정리한다는 관점으로 이해했다.

### 메모리 페이징

- 메모리 페이징: 프로세스 메모리를 일정한 크기의 page로 나누어 메모리와 디스크 사이에서 관리하는 방식

Prometheus는 최근 데이터를 메모리에 많이 올려두기 때문에 메모리 사용량 관리가 중요하다. 메모리가 부족하면 쿼리 성능이나 안정성에 영향을 줄 수 있다.

---

## 9. WAL과 데이터 저장 흐름

### WAL

- WAL(Write-Ahead Log): chunk로 flush되기 전 메모리에 있는 데이터를 장애 복구용으로 먼저 기록하는 로그

WAL은 Prometheus가 갑자기 종료되었을 때 메모리에 있던 데이터를 복구하기 위한 장치다. 디스크 block으로 완전히 저장되기 전의 데이터를 보호한다.

### Flush

- Flush: 메모리에 수집된 sample을 디스크의 block이나 chunk로 기록하는 작업

Flush는 메모리에 있는 데이터를 디스크 저장 구조로 넘기는 과정이다.

### 메모리 저장

- 메모리 저장: 최신 데이터 배치를 최대 약 2시간 동안 메모리에 보관해 쿼리 속도를 높이고 반복적인 디스크 쓰기를 줄이는 방식

최근 데이터는 자주 조회되므로 메모리에 두는 것이 유리하다. 대신 Prometheus의 메모리 사용량을 예측하고 관리해야 한다.

### 디스크 저장

- 디스크 저장: 일정 시간이 지나면 sample을 block 단위로 디스크에 기록해 장기 보관하는 방식

디스크에 저장된 데이터는 더 긴 기간의 조회와 보관에 사용된다.

### 불변 block

- 불변 block: 디스크에 저장된 뒤 직접 수정하지 않고 필요하면 삭제 표시나 새 block 생성으로 관리하는 block

불변 block 구조는 저장 안정성과 조회 효율에 도움이 된다. 기존 block을 계속 수정하지 않고 새 block을 만들거나 compaction으로 관리한다.

### 삭제 표시 파일

- 삭제 표시 파일: 데이터를 즉시 물리 삭제하지 않고 삭제 대상으로 표시하기 위해 사용하는 파일

삭제 요청이 들어와도 바로 데이터를 지우는 대신 삭제 표시를 남기는 방식으로 관리할 수 있다.

### 장애 복구

- 장애 복구: Prometheus가 재시작될 때 WAL을 재생해 메모리에 있던 미반영 데이터를 복구하는 과정

WAL이 있기 때문에 Prometheus 재시작 후에도 flush되지 않은 데이터를 어느 정도 복구할 수 있다.

---

## 10. Block 관리와 쿼리

### Block 생성

- Block 생성: 메모리에 수집된 sample을 기본 약 2시간 단위로 디스크에 flush해 block으로 만드는 과정

Prometheus는 시간 단위로 데이터를 block으로 나누어 저장한다. 이 구조는 시간 범위 조회에 유리하다.

### Block 병합

- Block 병합: 작은 block이 많아져 조회 성능이 떨어지지 않도록 여러 block을 적절히 합치는 작업

작은 block이 너무 많으면 쿼리할 때 많은 파일을 읽어야 한다. Block 병합은 저장 구조를 정리해 조회 효율을 높이는 과정이다.

### 쿼리 엔진

- 쿼리 엔진: PromQL 요청을 실행하고 필요한 chunk를 메모리나 디스크에서 읽어 결과를 계산하는 컴포넌트

쿼리 엔진은 사용자가 요청한 PromQL을 실제 데이터 조회와 계산으로 바꾼다. 쿼리가 복잡하거나 조회 범위가 넓으면 많은 리소스를 사용할 수 있다.

### 디스크 I/O

- 디스크 I/O: 쿼리나 저장 과정에서 디스크를 읽고 쓰는 작업으로, block 크기와 개수에 따라 성능에 영향을 받음

장기 범위 쿼리는 디스크에서 많은 block과 chunk를 읽어야 하므로 디스크 I/O 영향을 크게 받을 수 있다.

---

## 11. Prometheus Adapter 규칙

### Discovery

- Discovery: adapter가 Prometheus에서 어떤 metric을 custom metrics API로 노출할지 찾는 규칙

Discovery는 Prometheus 안의 많은 metric 중 어떤 metric을 Kubernetes custom metrics로 보여줄지 결정한다.

### Association

- Association: 특정 metric이 어떤 Kubernetes 리소스와 연결되는지 결정하는 규칙

HPA가 Pod나 Deployment 기준으로 metric을 해석하려면 metric과 Kubernetes 리소스의 관계를 알아야 한다.

### Naming

- Naming: Prometheus metric 이름과 Kubernetes custom metrics API 이름을 서로 변환하는 규칙

Prometheus의 metric 이름과 Kubernetes API에서 보이는 이름이 다를 수 있으므로 naming 규칙이 필요하다.

### Querying

- Querying: Kubernetes 리소스의 특정 metric 요청을 PromQL 쿼리로 변환하는 규칙

HPA가 custom metric을 요청하면 adapter는 이를 PromQL로 바꿔 Prometheus에 질의한다.

### Custom Metrics API

- Custom Metrics API: HPA가 CPU, 메모리 외 사용자 정의 메트릭을 조회할 때 사용하는 Kubernetes API

Custom Metrics API가 있어야 HPA가 Prometheus 기반 사용자 정의 메트릭을 스케일링 기준으로 사용할 수 있다.

---

## 12. Prometheus 알림

### Rule Manager

- Rule Manager: recording rule과 alert rule을 평가 주기마다 실행하고 알림 라이프사이클을 관리하는 Prometheus 내부 컴포넌트

Rule Manager는 rule file에 정의된 규칙을 주기적으로 평가한다. 알림 조건이 만족되는지도 여기서 판단한다.

### Recording Rule

- Recording Rule: 자주 쓰는 PromQL 계산 결과를 미리 저장해 쿼리 비용을 줄이는 규칙

복잡한 쿼리를 매번 실행하지 않고 미리 계산해두면 대시보드와 알림의 부하를 줄일 수 있다.

### Alert Rule

- Alert Rule: 특정 PromQL 조건이 만족될 때 알림을 발생시키도록 정의한 규칙

Alert Rule은 장애나 이상 징후를 감지하는 조건이다. 조건뿐 아니라 얼마나 오래 유지되어야 알림을 보낼지도 중요하다.

### Alertmanager

- Alertmanager: Prometheus alert rule에서 생성된 알림을 받아 이메일, 메신저, 티켓 시스템 등으로 전달하는 컴포넌트

Alertmanager는 알림 라우팅, 그룹화, 중복 제거, silence 같은 기능을 담당한다. Prometheus가 알림을 만들고, Alertmanager가 외부 채널로 보낸다고 이해했다.

### 알림 전송 흐름

- 알림 전송 흐름: alert rule 작성 후 Rule Manager가 조건을 평가하고 Alertmanager가 외부 채널로 알림을 전송하는 흐름

흐름으로 보면 `Alert Rule -> Rule Manager 평가 -> Alertmanager 전달 -> Slack, email, ticket 등 외부 채널` 순서다.

### 활성 상태

- 활성 상태: alert rule 조건이 아직 충족되지 않은 정상 상태

조건이 만족되지 않는 상태다. 아직 알림으로 이어지지 않는다.

### Pending

- Pending: alert 조건은 만족했지만 지정된 지속 시간에는 아직 도달하지 않은 준비 상태

Pending은 일시적인 튐으로 바로 알림이 나가지 않도록 막아준다. `for` 조건과 연결해서 이해할 수 있다.

### Firing

- Firing: alert 조건이 일정 시간 이상 유지되어 외부로 알림이 전송되는 상태

Firing 상태가 되면 실제 운영자가 확인해야 하는 알림으로 이어진다.

### 임계값

- 임계값: alert rule에서 정상과 비정상을 구분하기 위해 설정하는 기준 값

임계값은 너무 낮으면 알림이 많이 울리고, 너무 높으면 장애를 늦게 발견할 수 있다. 그래서 서비스 특성에 맞게 잡아야 한다.

---

## 13. Prometheus 운영 아키텍처

### High Cardinality Metric 피하기

- High Cardinality Metric 피하기: label 조합을 과도하게 늘리지 않아 Prometheus의 메모리와 쿼리 부담을 줄이는 운영 원칙

Prometheus 운영에서 가장 먼저 신경 써야 할 부분 중 하나다. 특히 사용자 ID, 요청 ID, 세션 ID 같은 값을 label로 넣는 것은 조심해야 한다.

### Sharding

- Sharding: Prometheus 수집 대상을 여러 인스턴스에 나누어 부하와 저장량을 분산하는 구조

단일 Prometheus가 모든 target과 metric을 감당하기 어려워지면 sharding을 고려할 수 있다.

### 수직 샤딩

- 수직 샤딩: 더 큰 리소스를 가진 Prometheus 인스턴스로 처리 능력을 키우는 확장 방식

CPU, memory, disk를 더 크게 주는 방식이다. 단순하지만 한계가 있고 비용도 커질 수 있다.

### 수평 샤딩

- 수평 샤딩: 여러 Prometheus 인스턴스가 서로 다른 target이나 metric을 나누어 수집하는 확장 방식

수평 샤딩은 부하를 여러 Prometheus 인스턴스로 나누는 방식이다. 대신 전체 데이터를 한 번에 조회하려면 추가 구조가 필요해질 수 있다.

### Federation

- Federation: 여러 Prometheus 서버의 시계열 데이터를 상위 Prometheus가 다시 scrape해 집계하는 연합 구조

Federation은 여러 Prometheus의 데이터를 상위 계층에서 모아 보는 구조다. 전체 시스템을 한 번에 보고 싶을 때 사용할 수 있다.

### 계층적 Federation

- 계층적 Federation: 하위 Prometheus 서버의 시계열을 상위 Prometheus 서버가 트리 구조로 수집하고 집계하는 방식

규모가 커질수록 Prometheus를 계층 구조로 나누어 운영할 수 있다. 다만 구조가 복잡해지므로 어떤 metric을 상위로 올릴지 설계가 필요하다.

---

## 14. Thanos와 장기 운영

### Thanos

- Thanos: 여러 Prometheus 인스턴스의 데이터를 글로벌 뷰로 조회하고 장기 보관, downsampling, 확장을 지원하는 운영 도구

Thanos는 Prometheus의 로컬 저장소 한계를 보완하는 도구다. 여러 Prometheus를 하나처럼 조회하고, object storage를 활용해 장기 보관을 지원한다.

### Global View

- Global View: 여러 Prometheus 서버의 데이터를 하나의 Prometheus처럼 통합해 조회하는 관점

Prometheus가 여러 개로 나뉘면 전체 상태를 보기 어려워진다. Global View는 분산된 데이터를 하나의 관점에서 보게 해준다.

### Thanos Sidecar

- Thanos Sidecar: Prometheus 옆에 붙어 로컬 데이터를 object storage로 업로드하고 query 계층과 연결하는 Thanos 구성 요소

Sidecar는 Prometheus와 함께 동작하면서 데이터를 외부 저장소로 보내거나 query 계층과 연결한다.

### Thanos Query

- Thanos Query(Queryer): 여러 Prometheus 또는 Thanos 컴포넌트의 데이터를 모아 하나의 쿼리 결과로 제공하는 컴포넌트

Thanos Query는 사용자의 쿼리를 받아 여러 데이터 소스에서 결과를 모아준다.

### Local Storage

- Local Storage: Prometheus가 기본으로 사용하는 로컬 디스크 기반 저장소

Prometheus는 기본적으로 로컬 디스크에 데이터를 저장한다. 간단하고 빠르지만 장기 보관과 내구성 측면에서는 한계가 있다.

### Local Storage의 한계

- Local Storage의 한계: 내구성이 낮고 수평 확장이 어려워 장기 보관과 대규모 운영에 제약이 생기는 문제

Prometheus 인스턴스나 노드에 문제가 생기면 로컬 데이터도 영향을 받을 수 있다. 장기 보관이나 대규모 조회에는 별도 구조가 필요하다.

### Downsampling

- Downsampling: 오래된 데이터를 낮은 해상도로 줄여 저장 비용과 쿼리 비용을 낮추는 방식

오래된 데이터는 초 단위 정밀도보다 긴 기간의 추세가 더 중요할 때가 많다. Downsampling을 통해 저장 비용을 줄이면서 장기 추세를 볼 수 있다.

### 장기 보관

- 장기 보관: Prometheus 로컬 저장소 한계를 넘어 object storage 등을 사용해 메트릭을 오래 저장하는 방식

장기 보관은 장애 분석, 추세 분석, 용량 계획에 도움이 된다. Prometheus 단독보다 Thanos 같은 도구와 함께 이야기되는 이유다.

---

## 15. 내 생각

이번 주는 Prometheus가 생각보다 많은 일을 한다는 느낌을 받았다. 단순히 메트릭을 저장하고 그래프로 보는 도구라고 생각했는데, 실제로는 scrape 설정, 서비스 디스커버리, TSDB 저장 구조, alert rule, adapter, sharding, Thanos까지 운영 범위가 꽤 넓었다.

특히 cardinality가 가장 기억에 남았다. label을 자유롭게 붙일 수 있다는 점은 편하지만, 잘못 붙이면 시계열이 폭발해서 Prometheus 자체가 불안정해질 수 있다. 메트릭을 만들 때도 운영 비용을 생각해야 한다는 점이 중요해 보였다.

궁금한 점은 실무에서는 Prometheus를 단일 인스턴스로 어느 정도까지 운영하고, 어느 시점부터 sharding이나 Thanos를 고려하는지다. 또 alert rule의 임계값은 처음에 어떤 기준으로 잡고 운영하면서 어떻게 조정하는지도 궁금하다.

---

## 16. 발표할 때 말할 내용

이번 주는 Prometheus의 흐름을 중심으로 짧게 이야기하면 좋을 것 같다.

1. Prometheus는 exporter endpoint를 Pull 방식으로 scrape해서 TSDB에 저장한다.
2. Kubernetes에서는 Prometheus Operator, ServiceMonitor, PodMonitor를 통해 동적인 수집 대상을 관리할 수 있다.
3. Prometheus 저장 구조는 sample, chunk, WAL, block, index로 이어진다.
4. Cardinality가 높아지면 메모리와 쿼리 성능에 큰 부담이 된다.
5. 운영 규모가 커지면 sharding, federation, Thanos 같은 확장 구조를 고려해야 한다.

발표 핵심 메시지는 "Prometheus는 메트릭 수집 도구이면서, 저장 구조와 운영 아키텍처까지 함께 이해해야 하는 시스템"이라고 정리하고 싶다.

---

## 17. 참고 자료

- 주 교재: 『모니터링의 새로운 미래 관측 가능성』
