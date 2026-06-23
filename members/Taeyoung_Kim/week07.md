### `Prometheus Operator`

- **배경**
    - Kubernetes 환경은 비영구적이고 임시적인 Pod를 기반으로 이루어져 있기 때문에 Prometheus를 구성하는 요소와 Prometheus의 메트릭 수집 대상들을 관리하기가 어려움
    - Prometheus는 시스템 내부의 yaml Config 파일을 기준으로 설정을 유지하는데, 이는 컨테이너 내부의 파일을 변경하기가 번거로운 Kubernetes 환경에서 Prometheus 관리
    - 따라서 위와 같은 문제를 해결하기 위해 나온 것이 Prometheus Operator
- **Prometheus Operator**
    - k8s 환경에서 Prometheus 관리를 자동화해 간단하게 구성할 수 있도록 도와주는 도구
    - https://github.com/prometheus-operator/prometheus-operator

- **구조**

![](./images/week07-1.png)

- Service들을 ServiceMonitor가 지속적으로 바라보고, Target을 Prometheus 서버로 전송
- 이러한 일련의 행위들을 Operator가 관리

### `프로메테우스 쿠버네티스 구성`

1. kube-prometheus 다운로드

```jsx
git clone https://github.com/prometheus-operator/kube-prometheus.git
```

2. CRD 및 namespace 생성

```jsx
kubectl create -f manifests/setup
```

3. Prometheus 관련 리소스 생성

```jsx
kubectl create -f manifests
```

4. 설치 확인

```jsx
kubectl get pods -n monitoring 
kubectl get svc -n monitoring 
kubectl get crd | grep monitoring.coreos.com
```

![](./images/week07-2.png)

5. 포트포워딩 구성

```jsx
	# Prometheus UI 접속
	kubectl -n monitoring port-forward svc/prometheus-k8s 9090
	# Alertmanager UI 접속
	kubectl -n monitoring port-forward svc/alertmanager-main 9093
```

### **`ServiceMonitor 기반 메트릭 수집 실습`**

1. 설치된 서비스모니터 확인

```jsx
kubectl get servicemonitor -n monitoring
```

![](./images/week07-3.png)

2. Sample Application 배포
- deployment.yaml

```jsx
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
  labels:
    app: sample-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: metrics-provider
        image: python:3.11-alpine
        ports:
        - name: http
          containerPort: 8080
        command:
        - python
        - -u
        - -c
        - |
          from http.server import BaseHTTPRequestHandler, HTTPServer
          import time

          class Handler(BaseHTTPRequestHandler):
              def do_GET(self):
                  if self.path == "/metrics":
                      body = f"""# HELP sample_app_requests_total Total requests
          # TYPE sample_app_requests_total counter
          sample_app_requests_total {int(time.time())}
          # HELP sample_app_up Sample app status
          # TYPE sample_app_up gauge
          sample_app_up 1
          """
                      self.send_response(200)
                      self.send_header("Content-Type", "text/plain; version=0.0.4")
                      self.end_headers()
                      self.wfile.write(body.encode())
                  else:
                      self.send_response(200)
                      self.end_headers()
                      self.wfile.write(b"sample app")

          HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
```

- service.yaml

```jsx
apiVersion: v1
kind: Service
metadata:
  name: sample-app
  labels:
    app: sample-app
spec:
  selector:
    app: sample-app
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 8080
  type: ClusterIP
```

- monitor.yaml

```jsx
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: sample-app
  labels:
    app: sample-app
spec:
  selector:
    matchLabels:
      app: sample-app
  endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

- 실행

```jsx
 kubectl apply -f deployment.yaml
 kubectl apply -f service.yaml
 kubectl apply -f monitor.yaml
```

3. 연결 상태 확인

```jsx
kubectl get endpoints sample-app
```

![](./images/week07-4.png)

4. 메트릭 정상 수집 여부 확인
- Prometheus Target

![](./images/week07-5.png)

- Prometheus Query

![](./images/week07-6.png)