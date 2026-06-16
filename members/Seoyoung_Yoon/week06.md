# 실습계획

**<Base 팀: 책 예제/기본 데모 중심>** 으로 선택해 책에 있는 **TNS(The New Stack)** 실습을 기반으로 진행할 예정입니다.

6주차: TNS(k8s 3티어) 애플리케이션 기반의 LGTM Stack 설치 후 메트릭 수집 (5장) </br>
7주차: 커스텀 대시보드 구축 </br>
8주차: 오픈텔레메트리 붙여서 로깅 고도화 (6장) </br>

# 책에 있는 실습
[Chapter 5.2 그라파나 o11y와 상관 관계](https://yohaim.medium.com/5-2-tns-%EC%98%88%EC%A0%9C-ba79f7291af)

# 뉴스택

[The New Stack 깃허브](https://github.com/grafana/tns)

<img width="722" height="392" alt="image" src="https://github.com/user-attachments/assets/46fe5cf0-da32-474b-a57a-020dd10bcb0f" />

TNS(The New Stack) 구조
- DB
- BE : App
- FE : Load Balancer


메트릭, 로그, 추적의 관측가능성을 데모하며, FE BE DB 3개의 레이어로 구성된 마이크로서비스

3개 레이어(데이터계층, 백엔드 계층, 프론트엔드 계층) 애플리케이션 쿠버네티스 클러스터에 배포하고, 모니터링

- 모니터링 구조 요약
1. 데이터 생성(TNS): Loadgen 파드가 app과 DB 파드에서 메트릭, 로그, 트레이스 데이터를 만들어낸다.
2. 데이터 수집: Loki. Prometheus, Tempo 모니터링 파드들이 데이터들을 실시간으로 가져온다.
3. 시각화: 이 데이터들은 그라파나로 전달되어 화면을 출력한다.

- Loadgen: 부하 발생기
- jaeger(예거): 트레이싱 표준 규격 도구,
- Promtail: 로그 배달

### 메트릭 Pull 방식

1. TNS 앱, 데이터베이스 파드들은 현재상태 값들(CPU, 요청 수 등)을 기록해둔다.
2. Prometheus 가 주기적으로 앱과 데이터베이스의 주소로 찾아가 데이터를 Pull 가져온다.
3. Prometheus는 이 데이터를 TSDB에 저장한다.

### 로그

1. TNS에 에러가 출력된다.
2. 쿠버네티스가 이 출력을 가로채 호스트 서버의 비밀 폴더 .log에 텍스트파일을저장한다.
3. Promtail이 폴더를 감시하고 있다가 새로운 로그가 뜨면 낚아챈다.

### 트레이스

1. Loadgen이 TNS에 요청(부하)을 보내면 앱은 내부 소스코드가 작동하면서 고유한 일련번호(Trace ID)를 생성한다.
2. 이 요청은 DB로 넘어갈때 Trace ID를 함께 가져간다.
3. 앱과 DB는 동작시간기록(예: App에서 0.1초 소요, DB에서 0.5초 소요)을 담은 Span을 만든다.
4. 이 Span은 jaeger로(Tempo) 들어간다. (규격에 맞게 저장)

뉴스택 TNS 는 추저그 메트릭 로그를 사용한 상관관계에 집중한다.

MLT는 프로파일을 추가하였으며, 오픈텔레메트리를 도입하였다. RED 대시보드를 제공하며, 다양한 마이크로 서비스를 제공한다.

# 실습
1. 미니쿠베, 헬름, 도커, kubectl 설치
- `e2-standard-4` (vCPU 4개, 메모리 16GB)
- 우분투 환경

```
# 패키지 업데이트
sudo apt update && sudo apt upgrade -y
```

```
# Docker 설치
sudo apt install -y docker.io
sudo systemctl enable --now docker

# 현재 사용자를 docker 그룹에 추가하여 권한 부여
sudo usermod -aG docker $USER

# 변경된 권한을 즉시 적용 (로그아웃 후 재접속 효과)
newgrp docker
```

```
# Kubectl 설치
# kubectl 바이너리 다운로드
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 시스템 경로에 설치 및 권한 부여
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

```
# Minikube 설치
# Minikube 바이너리 다운로드
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# 시스템 경로에 설치
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

```
# Helm 공식 설치
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

```
docker --version
kubectl version --client
minikube version
helm version

Docker version 20.10.24+dfsg1, build 297e128
Client Version: v1.36.1
Kustomize Version: v5.8.1
minikube version: v1.38.1
commit: c93a4cb9311efc66b90d33ea03f75f2c4120e9b0
version.BuildInfo{Version:"v3.21.0", GitCommit:"e0878d41b711792be60777fd65ad23a101e6b85f", GitTreeState:"clean", GoVersion:"go1.25.10"} 
```

2. minikube 클러스터 Docker 드라이버로 시작

블로그에 나온 none 드라이브 옛날 방식으로 Docker 드라이브를 사용

```sql
minikube start --driver=docker --memory=12000 --cpus=4
```

<img width="826" height="230" alt="image" src="https://github.com/user-attachments/assets/484c81ed-718b-41f4-9762-a4b9e6b7b713" />

3. 그라파나 헬름 레포 추가

<img width="700" height="93" alt="image" src="https://github.com/user-attachments/assets/ff418bd5-b2f5-490e-bf2c-c5e528f78f57" />


4. 템포(트레이싱) 설치

<img width="581" height="138" alt="image" src="https://github.com/user-attachments/assets/69567112-2932-491d-acab-03a30d10c05e" />


5. 프로메테우스 설치

```yaml
# 1. PVC 생성
kubectl apply -f prometheus-claim0-persistentvolumeclaim.yaml

# 2. 미니쿠베 내부로 설정 파일 전송
minikube cp prometheus.yml /tmp/hostpath-provisioner/default/prometheus-claim0/prometheus.yml

# 3. 서비스 및 디플로이먼트 배포
kubectl apply -f prometheus-service.yaml
kubectl apply -f prometheus-deployment.yaml
```

6. 모두 실행시키기(확인용)

```sql
# 1. 미니쿠베가 살아있는지 확인
minikube status

# 2. 미니쿠베 도커 컨테이너가 잘 돌고 있는지 확인
docker ps
# 미니쿠베 실행
minikube start
# TNS 배포
kubectl apply -f production/k8s-yamls/
# 확인
kubectl get pods -w
```

7. TNS 애플리에키션, 트레이싱 백엔드가 한 클러스터에서 실행

<img width="564" height="158" alt="image" src="https://github.com/user-attachments/assets/f3f3fc71-05aa-44de-837d-987cf8a676b1" />

<img width="1701" height="1340" alt="image" src="https://github.com/user-attachments/assets/8632cbd8-326f-444d-a951-603128747cb5" />

메인화면 
<img width="2048" height="1402" alt="image" src="https://github.com/user-attachments/assets/7e8958fd-4751-419e-ade7-aba21aab065e" />

그라파나와 각 서비스 연결주소

- **로키 연결 주소:** `http://loki:3100`
- **템포 연결 주소:** `http://tempo:3200`
- **프로메테우스 연결 주소:** `http://prometheus:9090`

<img width="2048" height="1357" alt="image" src="https://github.com/user-attachments/assets/04656959-4a4e-4b01-9dfb-f9423f40f906" />

<img width="2048" height="1433" alt="image" src="https://github.com/user-attachments/assets/317cb51f-8dc5-4857-b4df-7d33ddec4d2c" />

<img width="2048" height="1442" alt="image" src="https://github.com/user-attachments/assets/8d342167-1b90-4233-9f09-0cc926279970" />

<img width="780" height="526" alt="image" src="https://github.com/user-attachments/assets/cd2e9942-8d04-4848-b5d1-22ca076a07d2" />

- 로키
<img width="2048" height="1382" alt="image" src="https://github.com/user-attachments/assets/b5045c37-e254-4683-99a6-76c0d1b5b3d0" />

<img width="2048" height="635" alt="image" src="https://github.com/user-attachments/assets/fbfca3d0-3f1d-4721-9ec1-526ebf4c33ce" />

<img width="2048" height="770" alt="image" src="https://github.com/user-attachments/assets/9cb57ca9-351d-4f8a-a6db-0bef0dad8b23" />

로키 파생필드에 템포 설정!

- 템포
<img width="2048" height="1453" alt="image" src="https://github.com/user-attachments/assets/19120d43-10aa-46f9-8949-1b54499cca30" />

<img width="1350" height="326" alt="image" src="https://github.com/user-attachments/assets/1978a88d-76a0-4935-8fc0-0d2af81dfe5a" />


# 실습
1. 분산 트레이싱(템포 활용)
    
    사용자 요청이 마이크로 서비스 내부에서 어떻게 흘러가는지 확인
    
    Tempo 선택후 TNS 관련 트레이스를 검색한다. 하나의 트레이스를 클릭하면 Loadgen app db 순서로 이동한 타임라인 그래프가 나옴
    
    어디 구간에서 시간이 가장 오래걸렸는지 찾아낼 수 있다.
    
- 템포 확인
<img width="2048" height="1418" alt="image" src="https://github.com/user-attachments/assets/70ad73e7-2791-41c0-9267-8ce5da9640c4" />

<img width="2048" height="1445" alt="image" src="https://github.com/user-attachments/assets/4cd507e2-dd50-4d01-8d6f-b0d95183a71d" />

<img width="2048" height="1163" alt="image" src="https://github.com/user-attachments/assets/5dc47046-ce24-4f1e-b494-11192446a4b6" />


지표 해석 
- 데이터 저장 프로세스 총 3.75ms
- LB 3.75ms
- app 2.11ms
- db 188µs(마이크로초)

- 로그 확인
<img width="2048" height="1418" alt="image" src="https://github.com/user-attachments/assets/6058808d-28a6-4fcf-9722-b458e7469c87" />

<img width="2048" height="1418" alt="image" src="https://github.com/user-attachments/assets/f5ab0024-dd97-4053-ae82-ef83d5f62097" />

- 메트릭 데이터 정보
<img width="2048" height="1458" alt="image" src="https://github.com/user-attachments/assets/8684347e-0abb-41ba-bf54-9c2e78e951d1" />


