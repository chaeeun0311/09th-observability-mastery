# Week 07

## 1. 선택한 방향

- [ ] Base 실습
- [x] Project 적용

---

## 2. 진행 목표

- 라즈베리파이 2대(bastion/backend) 환경에 Prometheus + Grafana 모니터링 스택 구축
- Google의 Four Golden Signals(Latency, Traffic, Errors, Saturation) 관점에서 메트릭 수집 체계 설계
- Pi 특유의 운영 리스크(온도, 전력, SD카드 I/O)를 수치화하여 관측 가능하게 만들기

---

## 3. 실행 환경

| 항목 | 내용 |
|---|---|
| OS | Ubuntu 24.04 LTS (Raspberry Pi 5, 8GB × 2) |
| Docker | Docker Compose v2 |
| Prometheus | prom/prometheus:latest (bastion) |
| Grafana | grafana/grafana:latest (bastion) |
| 기타 | Node Exporter, cAdvisor, pi-metrics.sh |

---

## 4. 진행 내용

### 4-1. 메트릭 계층 설계

Google SRE의 Four Golden Signals를 기준으로 수집 대상을 정의했다.

| Golden Signal | 인프라 계층에서의 대응 | 수집기 |
|---|---|---|
| Latency | Disk I/O 지연, Network 지연 | Node Exporter |
| Traffic | Network RX/TX bytes | Node Exporter |
| Errors | 스로틀링, 전압 강하 | pi-metrics.sh |
| Saturation | CPU%, Memory%, Disk% | Node Exporter, cAdvisor |

### 4-2. 아키텍처

```
Backend (102)                    Bastion (106)
┌────────────────────┐          ┌────────────────────┐
│ Node Exporter:9100 │◄─scrape─│ Prometheus :9090    │
│ cAdvisor     :8082 │◄─scrape─│ Grafana    :3000    │
│ pi-metrics.sh      │          │ Node Exporter:9100  │
└────────────────────┘          │ pi-metrics.sh       │
                                └────────────────────┘
```

### 4-3. pi-metrics.sh 작성

vcgencmd은 Pi 펌웨어에 직접 접근하는 바이너리로 컨테이너 내부에서 실행 불가. 호스트에서 systemd timer(15초)로 실행하고, textfile collector를 통해 Node Exporter에 전달하는 구조로 해결했다.

수집 항목: CPU/GPU 온도, core/sdram 전압, 스로틀링 비트(under-voltage, throttled, freq_capped), ARM/core 클럭.

### 4-4. Docker Compose로 모니터링 통합

Node Exporter는 `--pid=host`, `--network=host` + `/proc`, `/sys` 마운트로 컨테이너에서도 호스트 메트릭 수집 가능. cAdvisor는 8082 포트로 매핑(8081은 Spring Actuator 사용 중).

모든 모니터링 컴포넌트를 Docker Compose로 관리하여 선언적 운영.

### 4-5. Prometheus + Grafana 배포

bastion에 Prometheus(retention 30일) + Grafana를 Docker Compose로 배포. datasource 자동 프로비저닝 설정.

---

## 5. 실행한 명령어 또는 설정

```bash
# pi-metrics.sh 핵심 (양쪽 Pi)
TEMP_RAW=$(cat /sys/class/thermal/thermal_zone0/temp)
TEMP=$(echo "scale=1; $TEMP_RAW / 1000" | bc)
echo "pi_cpu_temperature_celsius $TEMP"
# vcgencmd으로 전압, 스로틀링, 클럭 수집
# 임시파일 → mv 원자적 교체로 데이터 정합성 보장
```

```yaml
# Node Exporter (Docker, host network)
node-exporter:
  image: prom/node-exporter:latest
  pid: host
  network_mode: host
  volumes:
    - /proc:/host/proc:ro
    - /sys:/host/sys:ro
    - /var/lib/node_exporter/textfile_collector:/textfile:ro
  command:
    - '--collector.textfile.directory=/textfile'
```

```yaml
# prometheus.yml (bastion)
scrape_configs:
  - job_name: 'node-bastion'
    static_configs:
      - targets: ['host.docker.internal:9100']
  - job_name: 'node-backend'
    static_configs:
      - targets: ['192.168.123.102:9100']
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['192.168.123.102:8082']
```

---

## 6. 확인한 결과

- Prometheus targets: node-bastion ✅, node-backend ✅, cadvisor ✅, prometheus ✅
- pi-metrics.sh 정상 수집: CPU 32.5°C, core 0.8592V, 스로틀링 0, ARM 2.3GHz
- cAdvisor: 46개 container metric series 수집
- bastion → backend 포트(9100, 8082) 접근 정상

---

## 7. 발생한 문제와 해결 과정

| 문제 | 원인 | 해결 |
|---|---|---|
| node-exporter, cadvisor 안 뜸 | docker-compose.yml에 서비스 미추가 (GitHub에만 올리고 Pi 미반영) | git pull 후 docker compose up -d |
| cAdvisor 포트 충돌 | 8081을 Spring Actuator가 사용 중 | 8082:8080으로 변경 |
| HDD 인식 실패 (0B) | Pi USB 전력 부족으로 HDD 스핀업 실패 | SSD 전환 또는 전원 공급 USB 허브 필요 |

---

## 8. Observability 관점에서 배운 점

- **Golden Signals의 Saturation**: Pi는 8GB RAM + SD카드라는 물리적 한계가 있어, Saturation 메트릭(CPU%, Memory%, Disk%)이 일반 서버보다 훨씬 빠르게 임계점에 도달한다. 지속적 관측이 필수.
- **Pi 전용 메트릭의 가치**: 전력 부족 시 자동 다운클럭이 발생하여 서비스 성능이 저하되는데, `pi_under_voltage`와 `pi_clock_hz`가 없으면 원인 파악이 불가능하다.
- **textfile collector 패턴**: Prometheus 생태계에 exporter가 없는 메트릭도 셸 스크립트 + textfile collector로 수집 가능. 원자적 파일 교체(tmp → mv)로 정합성 보장.

---

## 9. 다음에 개선하고 싶은 점

- Application/DB 레벨 모니터링 추가 (Golden Signals의 Latency, Errors 보강) → 2편에서 진행
- Grafana 알림 규칙 등록 + Discord 연동
- UFW 방화벽으로 모니터링 포트 접근 제한