# Week 08

## 1. 선택한 방향

- [ ] Base 실습
- [x] Project 적용

---

## 2. 진행 목표

- 1편에서 구축한 인프라 모니터링 위에 Application/DB 계층 모니터링을 추가하여 Four Golden Signals 전 영역 커버
- DB exporter를 통한 slow query, 데드락, 커넥션 관측 체계 구축
- CI/CD 파이프라인 개선 + DB bind mount 전환
- 커스텀 Grafana 대시보드 작성

---

## 3. 실행 환경

| 항목 | 내용 |
|---|---|
| OS | Ubuntu 24.04 LTS (Raspberry Pi 5, 8GB × 2) |
| Docker | Docker Compose v2 |
| Prometheus | prom/prometheus:latest (bastion) |
| Grafana | grafana/grafana:latest (bastion) |
| 기타 | Spring Actuator + Micrometer, postgres-exporter, mongodb-exporter |

---

## 4. 진행 내용

### 4-1. Golden Signals 매핑 완성

1편에서 Saturation과 일부 Traffic을 커버했고, 2편에서 나머지를 채웠다.

| Golden Signal | 1편 (인프라) | 2편 (앱/DB) |
|---|---|---|
| Latency | Disk I/O, Network | **HTTP p95 응답시간, PG/Mongo 쿼리 지연** |
| Traffic | Network RX/TX | **HTTP RPS, DB TPS, Mongo ops/sec** |
| Errors | 스로틀링, 전압 강하 | **5xx 에러율, PG 데드락, rollback 비율** |
| Saturation | CPU%, Mem%, Disk% | **HikariCP 커넥션풀, PG 커넥션, JVM 힙** |

### 4-2. DB Exporter 추가

docker-compose.yml에 postgres-exporter와 mongodb-exporter를 추가했다.

PostgreSQL에 `pg_stat_statements` 확장을 활성화하여 쿼리별 실행 통계(평균 실행시간, 호출 횟수)를 수집 가능하게 했다.

### 4-3. Spring Boot Actuator 확인

application.yml에 이미 Prometheus 엔드포인트가 설정되어 있었다. management port 8081에서 `/actuator/prometheus`로 JVM, HTTP, HikariCP 메트릭을 노출.

### 4-4. CI/CD 파이프라인 개선

기존 문제: backend에 git repo를 수동 clone하고 수동 배포.

개선: bastion runner에서 빌드 → `docker save | gzip | ssh docker load`로 이미지 전송 → `scp`로 compose + .env 전송 → `ssh`로 자동 배포.

backend에 git repo 불필요. GitHub push만으로 전체 배포 자동화.

### 4-5. DB bind mount 전환

named volume → bind mount로 전환. `DATA_DIR` 환경변수로 경로를 제어하여 향후 HDD 연결 시 `.env` 한 줄 변경으로 전환 가능하게 설계.

기존 volume 데이터를 `cp -a`로 복사하여 무손실 마이그레이션.

### 4-6. 커스텀 대시보드 작성

커뮤니티 대시보드가 exporter 버전 호환 문제로 동작하지 않아 직접 작성. Golden Signals 기준으로 패널을 배치했다.

**Observability 대시보드**: Overview 게이지 6개 → CPU/Memory 추이 → Pi 온도/전압/클럭 → Disk/Network I/O

**Server 대시보드**: Overview 게이지 8개 → HW → Docker 컨테이너 → PostgreSQL(커넥션, TPS, 데드락, 캐시 히트율, slow query) → MongoDB(커넥션, CRUD ops, read/write latency) → Spring Boot(HTTP RPS, p95, JVM, HikariCP, GC, slow endpoint)

---

## 5. 실행한 명령어 또는 설정

```yaml
# postgres - slow query 추적 활성화
postgres:
  command: ["postgres", "-c", "shared_preload_libraries=pg_stat_statements", "-c", "pg_stat_statements.track=all"]

# DB exporter
postgres-exporter:
  image: prometheuscommunity/postgres-exporter:latest
  environment:
    DATA_SOURCE_NAME: "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable"
  ports:
    - "9187:9187"

mongodb-exporter:
  image: percona/mongodb_exporter:0.43.1
  command: ['--mongodb.uri=${MONGO_URI}', '--collect-all', '--compatible-mode']
  ports:
    - "9216:9216"
```

```yaml
# bind mount (DATA_DIR로 경로 제어)
volumes:
  - ${DATA_DIR:-./data}/postgres:/var/lib/postgresql/data
# 지금: ./data/ (SD카드)
# HDD 연결 시: DATA_DIR=/mnt/hdd
```

```yaml
# CI/CD 핵심 (deploy.yml)
- run: docker build -t deadlock-server:latest .
- run: docker save deadlock-server:latest | gzip | ssh $BACKEND_HOST "gunzip | docker load"
- run: scp docker-compose.yml .env $BACKEND_HOST:$DEPLOY_DIR/
- run: ssh $BACKEND_HOST "cd $DEPLOY_DIR && docker compose up -d"
```

---

## 6. 확인한 결과

- Prometheus targets 7개 중 6개 UP (spring-boot만 app unhealthy로 DOWN)
- postgres-exporter: pg_stat_activity, pg_stat_database, pg_database_size 등 수집 정상
- mongodb-exporter: mongodb_ss_connections, mongodb_ss_opcounters, mongodb_ss_opLatencies 수집 정상
- CI/CD: GitHub push → bastion 빌드 → backend 자동 배포 + Discord 알림 정상
- DB 마이그레이션: named volume → bind mount 전환 후 데이터 정상 유지
- 커스텀 대시보드 2개 임포트 후 데이터 표시 확인

---

## 7. 발생한 문제와 해결 과정

| 문제 | 원인 | 해결 |
|---|---|---|
| workflow가 runner 대기에서 멈춤 | 라벨을 `dev-deadlock`으로 잘못 기입 (정답: `pi-ops`) | `runs-on: [self-hosted, pi-ops]`로 수정 |
| mongodb-exporter pull 실패 | `percona/mongodb_exporter:2.43.1` 존재하지 않음 | `0.43.1`로 수정 |
| docker compose down 시 network 삭제 불가 | AI compose가 같은 네트워크를 external로 참조 | AI 먼저 중지 → server down → 재시작. `COMPOSE_PROJECT_NAME` 고정으로 네트워크명 유지 |
| 커뮤니티 대시보드 미표시 | exporter 버전/메트릭명 호환 문제 | 커스텀 대시보드 JSON 직접 작성 |
| 프로젝트명 불일치로 기존 volume 분리 우려 | ~/deploy에서 실행 시 프로젝트명이 `deploy`로 변경 | `.env`에 `COMPOSE_PROJECT_NAME=deadlock-server` 추가 |

---

## 8. Observability 관점에서 배운 점

- **Golden Signals로 대시보드 구조화**: 패널을 무작정 나열하면 "뭘 봐야 하지?"가 된다. Latency(p95 응답시간, 쿼리 지연), Traffic(RPS, TPS), Errors(5xx, 데드락), Saturation(커넥션풀, 메모리) 기준으로 배치하니 장애 시 어떤 Signal이 이상한지 바로 보인다.
- **Overview → Drill-down 구조**: 상단 게이지로 1초 만에 전체 상태 파악 → 이상 시 아래 상세 패널로 원인 추적. 이 구조가 운영 판단 속도를 높인다.
- **DB 메트릭의 중요성**: PG Cache Hit Ratio가 99% 미만이면 메모리 부족 징후, 데드락 발생은 트랜잭션 설계 문제를 의미한다. 이런 메트릭 없이는 "왜 느리지?"에 답할 수 없다.
- **IaC로 모니터링 관리**: docker-compose.yml, prometheus.yml, 대시보드 JSON까지 Git으로 관리하면 설정 변경 이력 추적이 가능하다.

---

## 9. 다음에 개선하고 싶은 점

- Spring Boot app unhealthy 원인 해결 → 애플리케이션 메트릭 정상화
- Grafana 알림 규칙 등록 (CPU 과열, 전력 부족, 5xx 급증, 데드락) + Discord 연동
- HDD 연결 후 `DATA_DIR=/mnt/hdd`로 DB 데이터 이전
- Loki 추가로 로그 수집까지 통합 (Metrics + Logs 상관분석)