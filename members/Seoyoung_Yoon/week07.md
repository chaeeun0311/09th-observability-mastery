# LGTM 발표

- LGTM 환경 구축 완료
- TNS 3티어 구성요소 (App, DB)의 메트릭 정보를 대시보드로 구성한다.

  a. 통합 대시보드 </br>
  b. 서비스 상태 대시보드 </br>
  c. 인프라 쿠버네티스 대시보드 </br>

1. 통합 대시보드 생성
  <img width="2048" height="1469" alt="image" src="https://github.com/user-attachments/assets/ad65230c-e66b-4879-b1ef-fb40a3103eff" />

2. 대시보드 이름 수정

  <img width="2048" height="1372" alt="image" src="https://github.com/user-attachments/assets/96e34374-4d8d-42b7-b47b-74ff62612870" />

3. 패널 수정

  `sum(rate(tns_request_duration_seconds_count[1m]))` 총 처리량
  <img width="2048" height="1447" alt="image" src="https://github.com/user-attachments/assets/24edda8d-659f-4417-bbad-a8071f663a44" />

상태 메트릭 설정

<img width="2048" height="1454" alt="image" src="https://github.com/user-attachments/assets/58ca0464-0d84-4e03-9676-e5119f0add17" />

Calculation Last로 설정하여 최근 값 조회로 수정

<img width="2048" height="1378" alt="image" src="https://github.com/user-attachments/assets/c3885afb-a948-4c27-bd92-dc062b9ae283" />

상태 메트릭 출력 값, 색 수정

<img width="2048" height="1358" alt="image" src="https://github.com/user-attachments/assets/f33359dc-259e-4bb8-95d5-a9cb4d32a3fc" />

<img width="2048" height="1379" alt="image" src="https://github.com/user-attachments/assets/663cd951-3d7b-4497-b08f-ce7b85e8521e" />

에러가 계속 보이는 이유: Grafana TNS 데모 애플리케이션이 일부러 에러를 발생시키도록 설계되었기 때문

4. 서비스 상태 대시보드

변수 생성
<img width="2048" height="1376" alt="image" src="https://github.com/user-attachments/assets/c84141d2-75ca-4e67-a6fa-c211995053db" />

<img width="2048" height="1376" alt="image" src="https://github.com/user-attachments/assets/70fb30e5-4f27-4cd5-ba29-9b7359d58435" />

애플리케이션, DB 확인 가능

<img width="2048" height="1458" alt="image" src="https://github.com/user-attachments/assets/6bdb4196-f7a4-4dad-94a5-54e257d1d0c0" />

5. 쿠버네티스 대시보드

프로메테우스에 k8s 메트릭 추가

```yaml
kubectl edit configmap prometheus-config -n default

- job_name: 'kube-state-metrics'
        static_configs:
          - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
```

쿠버네티스 상태 메트릭 값 추가

인프라 쿠버네티스 모니터링 구축 완료
<img width="2048" height="1365" alt="image" src="https://github.com/user-attachments/assets/759713f8-fdb6-4a69-98a6-bfe6ebc7fc92" />
