# 3장

## 프로메테우스

프로메테우스는 단순한 모니터링과 운영에 그치지 않고 많은 기능을 제공한다.

단순히 메트릭을 수집하는 것을 넘어, 시계열 데이터 저장(TSDB), 서비스 디스커버리, 알람, 오토스케일링 연동 등 다양한 기능을 제공한다.

## 프로메테우스 생태계

#### 1. 프로메테우스 Operator

- Operator가 새로운 쿠버네티스 리소스 타입(crd)을 추가하고
- 그 리소스들을 감시하면서, 실제 prometheus 설정을 자동 생성하는 구조
- Prometheus Operator는 프로메테우스 관련 리소스를 쿠버네티스 방식(CRD)으로 관리할 수 있게 해주는 컨트롤러이다.
    - ServiceMonitor
    - PodMonitor
    - PrometheusRule
    - Alertmanager
- 특히 ServiceMonitor와 PodMonitor는 서비스 디스커버리 기능을 제공한다.
- 프로메테우스 Operator는 클러스터의 서비스와 파드 변화를 지속적으로 감시하며, 새로운 타겟이 생성되거나 제거되면 프로메테우스 scrape 설정을 자동으로 갱신한다.
- 즉, 운영자가 Prometheus 설정 파일을 직접 수정하지 않아도 동적으로 모니터링 대상이 반영된다.

**ServiceMonitor**

ServiceMonitor는 어떤 서비스를 Prometheus가 수집(scrape)할지를 선언적으로 정의하는 CRD이다.

주로 label selector를 사용하여 특정 서비스를 선택한다.

예를 들어:

- `app=networkdoctor-agent`
- `monitoring=enabled`

와 같은 라벨을 가진 서비스를 자동으로 발견하여 `/metrics` 엔드포인트를 scrape 대상으로 등록할 수 있다.

즉, "어떤 서비스의 어떤 포트를 Prometheus가 수집할 것인가"

#### 2. 프로메테우스 Exporter

- Exporter는 특정 시스템이나 애플리케이션의 메트릭을 수집하여 `/metrics` HTTP 엔드포인트로 노출하는 에이전트이다.
- Prometheus는 이 엔드포인트를 주기적으로 scrape하여 메트릭을 수집한다.
- 기본적으로 제공해주는 exporter 외에 애플리케이션 특화 메트릭을 수집하기 위해 커스텀 Exporter를 개발할 수 있다.
- Prometheus는 이를 위한 다양한 Client Library 및 SDK를 제공한다.

#### 3. 프로메테우스 Adapter

- Prometheus Adapter는 Prometheus 메트릭을 Kubernetes Custom Metrics API 형태로 변환하여 제공하는 컴포넌트이다.
- 기본 Kubernetes Metrics Server는 CPU, Memory 같은 기본 메트릭만 제공한다.
- 하지만 다음과 같은 커스텀 메트릭은 기본 Metrics Server만으로는 사용할 수 없다.
    - HTTP 요청 수
    - 네트워크 패킷 드롭률
    - 큐 길이
    - 사용자 정의 애플리케이션 메트릭
- 이때 Prometheus Adapter를 사용하면 Prometheus에 저장된 메트릭을 HPA(Horizontal Pod Autoscaler)에서 사용할 수 있다.

```markdown
# 다음과 같은 흐름으로 커스텀 메트릭 기반 오토스케일링을 구현할 수 있다.
Exporter → Prometheus → Adapter → HPA
```

## 시계열 데이터베이스(Time Series Database)

Prometheus는 Pull 방식이다.

전체 흐름은 다음과 같다.

1. application이 Prometheus client 또는 OTel을 통해 메트릭을 생성하고,
2. http 엔드포인트로 메트릭(ex: /metrics)을 노출
3. ServiceMonitor가 scrape 대상을 정의
4. Operator가 ServiceMonitor를 감지하여 Prometheus 설정에 반영
5. Prometheus Server가 주기적으로 해당 엔드포인트를 scrape
6. 수집한 메트릭을 TSDB(Time Series Database)에 저장
7. Grafana 등에서 조회 및 시각화

→ Prometheus Exporter가 /metrics 경로를 통해 데이터를 제공하면 프로메테우스 서버가 pull 방식으로 익스포터에서 그 데이터를 수집하여 시계열 데이터베이스(TSDB)에 저장한다.

### TSDB 특징

Prometheus TSDB는 시계열 데이터 저장에 최적화되어 있다.

주요 특징은 다음과 같다.

- 데이터를 시계열(Time Series) 형태로 저장
- 일정 시간 단위로 샘플을 청크(chunk)로 압축 저장
- 여러 청크를 블록(block) 단위로 관리
- 인덱스를 통해 빠른 조회 지원
- 최근 데이터는 메모리에 유지하고 장기 데이터는 디스크에 저장

### TSDB와 WAL

Prometheus는 데이터 안정성을 위해 WAL(Write Ahead Log)을 사용한다.

메트릭이 바로 block으로 저장되는 것이 아니라:

1. 먼저 WAL에 기록
2. 이후 메모리의 chunk에 반영
3. 일정 조건이 되면 block 형태로 디스크에 flush

되는 방식으로 동작한다.

즉 WAL은 장애 발생 시 데이터 유실을 최소화하기 위한 로그이다.

Prometheus가 비정상 종료되더라도, 재시작 시 WAL을 기반으로 데이터를 복구할 수 있다.