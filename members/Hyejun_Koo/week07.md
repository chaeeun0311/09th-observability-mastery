# 6/14 일

템플릿 형식: 프로젝트

# handDoc 모니터링 적용 실습 정리

## 0. 기본 정보

- 이름: 구혜준
- 주차:
- 진행 주제: handDoc 프로젝트에 Prometheus + Grafana 기반 모니터링 적용
- 실습 대상:
    - Spring Boot 백엔드 서버
    - FastAPI AI 서버
    - Prometheus
    - Grafana

---

## 1. 이번 주에 해본 것

이번 주에는 handDoc 프로젝트에 Prometheus와 Grafana 기반의 모니터링 환경을 붙여보았다.

handDoc은 Spring Boot 백엔드와 FastAPI 기반 AI 서버가 함께 동작하는 구조이기 때문에, 두 서버의 상태를 각각 확인할 수 있도록 모니터링 구성을 나누어 진행했다. Spring Boot 서버는 Actuator와 Micrometer Prometheus를 이용해 `/actuator/prometheus` 엔드포인트로 메트릭을 노출했고, FastAPI 서버는 `prometheus-client`를 이용해 `/metrics` 엔드포인트로 메트릭을 노출했다.

먼저 FastAPI 서버에서 `/metrics`가 정상적으로 열리는지 확인했다.

```powershell
curl.exe http://localhost:8000/metrics
```

실행 결과, Python 런타임 관련 메트릭뿐만 아니라 handDoc에서 직접 정의한 FastAPI 관련 메트릭도 함께 출력되는 것을 확인했다. 예를 들어 FastAPI 요청 수, WebSocket 연결 수, WebSocket 메시지 수, 수어 프레임 처리 지연시간, AI 추론 지연시간 관련 메트릭이 노출되었다.

[FastAPI `/metrics` 출력 화면]

![image.png](image.png)

```markdown
![FastAPI metrics 출력 화면](./images/fastapi-metrics.png)
```

이후 Spring Boot 서버도 실행한 뒤, Actuator health endpoint와 Prometheus endpoint가 정상적으로 동작하는지 확인했다.

```powershell
curl.exe http://localhost:8080/actuator/health
curl.exe http://localhost:8080/actuator/prometheus
```

Spring Boot에서는 `system_cpu_usage`, `spring_security_http_secured_requests_seconds`, `tomcat_sessions_*` 등 JVM, Spring Security, Tomcat 관련 메트릭이 정상적으로 출력되는 것을 확인했다.

[Spring Boot `/actuator/prometheus` 출력 화면]

![image.png](image%201.png)

```markdown
![Spring Boot actuator prometheus 출력 화면](./images/spring-actuator-prometheus.png)
```

그다음 `handdoc-observability` 폴더에 Prometheus와 Grafana를 실행하기 위한 Docker Compose 환경을 구성했다.

```powershell
docker compose -f .\handdoc-observability\docker-compose.yml up -d
```

실행 후 Prometheus와 Grafana 컨테이너가 정상적으로 올라온 것을 확인했다.

```powershell
docker compose -f .\handdoc-observability\docker-compose.yml ps
```

Prometheus 설정에서는 FastAPI와 Spring Boot의 메트릭 엔드포인트를 scrape하도록 구성했다. 로컬에서 실행 중인 서버를 Docker 컨테이너 내부의 Prometheus가 접근해야 했기 때문에, target 주소는 `localhost`가 아니라 `host.docker.internal`을 사용했다.

예시 설정은 다음과 같다.

```yaml
scrape_configs:
  - job_name: "fastapi"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["host.docker.internal:8000"]

  - job_name: "spring-boot"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["host.docker.internal:8080"]
```

이후 Prometheus Targets 화면에서 FastAPI와 Spring Boot가 모두 `UP` 상태로 표시되는 것을 확인했다.

[Prometheus Targets 화면]

![image.png](image%202.png)

```markdown
![Prometheus Targets UP 화면](./images/prometheus-targets-up.png)
```

마지막으로 Grafana에서 Prometheus를 Data source로 연결하고, handDoc 모니터링 대시보드를 구성했다. 대시보드에는 서비스 상태, Spring Boot CPU 사용률, Spring Boot 요청량, FastAPI scrape 상태 등을 확인할 수 있는 패널을 추가했다.

[ Grafana 대시보드 화면]

![image.png](image%203.png)

```markdown
![HandDoc Grafana Dashboard](./images/grafana-dashboard.png)
```

---

## 2. 새로 알게 된 점

이번 실습을 통해 Prometheus는 애플리케이션이 직접 데이터를 보내는 방식이 아니라, Prometheus가 정해진 주기마다 각 서비스의 메트릭 엔드포인트를 직접 긁어가는 pull 방식으로 동작한다는 점을 알게 되었다.

FastAPI에서는 `/metrics`, Spring Boot에서는 `/actuator/prometheus`처럼 각 애플리케이션이 Prometheus 형식의 메트릭을 노출해야 하고, Prometheus는 이 엔드포인트를 scrape해서 시계열 데이터로 저장한다.

또한 Docker 컨테이너 안에서의 `localhost` 개념도 확실히 이해하게 되었다. 처음에는 Prometheus 설정에서 `localhost:8000`, `localhost:8080`을 사용하면 될 것이라고 생각했지만, Prometheus가 Docker 컨테이너 안에서 실행되는 경우 `localhost`는 내 PC가 아니라 Prometheus 컨테이너 자기 자신을 의미한다. 따라서 컨테이너에서 로컬 PC의 FastAPI와 Spring Boot에 접근하려면 `host.docker.internal:8000`, `host.docker.internal:8080`을 사용해야 했다.

Spring Boot에서는 Actuator와 Micrometer Prometheus registry의 역할도 구분할 수 있었다. Actuator는 애플리케이션의 상태와 운영 정보를 외부로 노출하는 기능이고, Micrometer Prometheus registry는 그 정보를 Prometheus가 읽을 수 있는 형식으로 변환해주는 역할을 한다.

Grafana에서는 Prometheus에 저장된 메트릭을 PromQL로 조회해 시각화한다는 점을 실습했다. `up`, `system_cpu_usage`, `spring_security_http_secured_requests_seconds_count`, `scrape_duration_seconds` 같은 지표를 통해 서비스가 살아있는지, CPU 사용률은 어느 정도인지, 요청은 들어오고 있는지 등을 확인할 수 있었다.

---

## 3. 막힌 부분이나 같이 보고 싶은 질문

첫 번째로 막힌 부분은 FastAPI `/metrics` 확인 과정이었다. 처음에 다음 명령어를 실행했을 때 연결 실패가 발생했다.

```powershell
curl.exe http://localhost:8000/metrics
```

이 문제의 원인은 `/metrics` 코드 문제가 아니라 FastAPI 서버가 실행 중이지 않았기 때문이었다. FastAPI 서버를 다시 실행한 뒤에는 `/metrics`가 정상적으로 출력되었다.

두 번째로 막힌 부분은 Spring Boot 서버 상태 확인이었다. 처음에는 Spring Boot target이 unhealthy처럼 보였지만, 실제 원인은 Spring Boot가 8080 포트에서 실행되고 있지 않은 상태였다. 이후 backend 폴더에서 `bootRun`을 실행하자 정상적으로 Tomcat이 8080 포트에서 시작되었고, `/actuator/prometheus`도 정상적으로 응답했다.

세 번째로는 Gradle 실행 위치 문제가 있었다. 프로젝트 루트에서 다음 명령어를 실행했을 때 `gradlew`를 찾을 수 없다는 에러가 발생했다.

```powershell
.\gradlew bootRun
```

이는 `gradlew`가 프로젝트 루트가 아니라 backend 폴더 내부에 있었기 때문에 발생한 문제였다. Gradle Wrapper가 있는 폴더로 이동한 뒤 실행해야 했다.

네 번째로는 Grafana에서 FastAPI 요청량을 조회하는 PromQL이 바로 표시되지 않는 문제가 있었다.

```
sum(rate(fastapi_http_requests_total[1m]))
```

이 쿼리가 바로 표시되지 않은 이유는 아직 충분한 요청 샘플이 쌓이지 않았거나, 1분 범위 안에 Prometheus scrape 데이터가 충분하지 않아 `rate()` 계산이 되지 않았기 때문으로 보인다. 그래서 임시로 FastAPI의 상태를 확인할 수 있는 다음 지표를 사용했다.

```
up{job="fastapi"}
```

또는 FastAPI scrape 자체가 정상적으로 이루어지고 있는지 확인하기 위해 다음 지표도 사용할 수 있었다.

```
scrape_duration_seconds{job="fastapi"}
```

같이 보고 싶은 질문은 FastAPI에서 직접 정의한 `fastapi_http_requests_total` 카운터가 실제 API 요청에서 정확히 증가하는지이다. 특히 `/metrics`나 `/docs` 요청이 카운터에서 제외되어 있는지, WebSocket 요청에서도 별도 메트릭이 정상적으로 증가하는지 확인해보고 싶다.

---

## 4. 다음에 이어서 해볼 것

다음에는 Grafana 대시보드를 더 handDoc 서비스에 맞게 정리할 예정이다. 현재는 FastAPI와 Spring Boot가 Prometheus에 정상적으로 연결되는지 확인하는 데 집중했기 때문에, 이후에는 실제 운영 상황을 더 잘 볼 수 있는 지표를 중심으로 대시보드를 구성할 계획이다.

Spring Boot 쪽에서는 API별 요청 수, 응답 시간, 에러율을 확인할 수 있도록 PromQL을 추가해볼 예정이다. 이를 통해 어떤 API에 요청이 많이 들어오는지, 특정 API의 응답 시간이 느려지는지, 에러가 발생하는지 확인할 수 있다.

FastAPI 쪽에서는 실제 수어 인식 WebSocket 요청을 발생시켜 커스텀 메트릭이 정상적으로 증가하는지 확인할 예정이다. 특히 handDoc의 AI 서버는 실시간으로 프레임을 처리하고 추론을 수행하기 때문에, 다음과 같은 지표를 중요하게 볼 수 있을 것 같다.

```
ai_sign_frames_total
ai_sign_inference_total
ai_sign_frame_processing_duration_seconds
ai_sign_inference_duration_seconds
fastapi_ws_connections_total
fastapi_ws_messages_total
fastapi_ws_errors_total
```

이후에는 평균 지연시간뿐만 아니라 P95 지연시간도 Grafana에서 확인할 수 있도록 구성할 예정이다.

```
histogram_quantile(0.95, sum(rate(ai_sign_inference_duration_seconds_bucket[5m])) by (le))
```

추가로 가능하다면 alert rule도 설정해보고 싶다. 예를 들어 Spring Boot나 FastAPI가 `DOWN` 상태가 되거나, 응답 시간이 일정 기준 이상으로 증가하거나, 에러율이 높아질 때 알림을 발생시키는 방식으로 확장할 수 있다.

최종적으로는 handDoc의 Spring Boot 백엔드와 FastAPI AI 서버를 Prometheus와 Grafana로 함께 관측할 수 있는 구조를 완성하고, 대시보드 캡처와 설정 파일을 정리해 포트폴리오와 프로젝트 문서에 포함할 예정이다.
