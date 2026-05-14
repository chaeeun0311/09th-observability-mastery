# 모니터링 정복: Zero부터 시작하는 Observability

CloudClub 시즌2 스터디 **“모니터링 정복: Zero부터 시작하는 Observability”** 레포지토리입니다.

이 스터디는 Prometheus, Grafana 같은 도구 사용법만 익히는 시간이 아닙니다. Observability의 기본 개념을 이해하고, 실제 운영 상황에서 **어떤 데이터를 보고 어떻게 판단할지** 함께 연습하는 것을 목표로 합니다.

---

## 1. 한눈에 보기

| 항목 | 내용 |
|---|---|
| 스터디명 | 모니터링 정복: Zero부터 시작하는 Observability |
| 진행 기간 | 총 8주 |
| 진행 시간 | 매주 목요일 21:00 ~ 22:30 |
| 진행 방식 | 책 기반 학습, 과제 정리, 랜덤 발표, Q&A, 토론, 후반부 실습 |
| 주 교재 | 『모니터링의 새로운 미래 관측 가능성』 |
| 주요 도구 | Prometheus, Grafana, OpenTelemetry, Kubernetes 등 |
| 과제 제출 | `members/{영문이름}/weekXX.md` |

과제 제출, 브랜치, Pull Request 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고합니다.

---

## 2. 스터디 소개

현대적인 서비스 운영 환경에서는 단순히 서버가 살아 있는지 확인하는 것만으로는 충분하지 않습니다.

서비스가 느려졌는지, 특정 API에서 에러가 증가했는지, 사용자 요청이 어느 구간에서 지연되는지, 장애 상황에서 어떤 데이터를 먼저 확인해야 하는지 판단할 수 있어야 합니다.

이 스터디에서는 정현석 저자의 『모니터링의 새로운 미래 관측 가능성』을 중심으로 Observability의 기본 개념을 학습하고, 발표와 토론을 통해 운영자/SRE/DevOps 관점에서 해석하는 연습을 진행합니다.

후반부에는 Prometheus, Grafana, OpenTelemetry, Kubernetes 환경 등을 활용한 가벼운 실습 또는 개인 프로젝트 적용을 진행합니다.

---

## 3. 스터디 목표

- Observability의 기본 개념을 이해한다.
- Monitoring과 Observability의 차이를 설명할 수 있다.
- Metrics, Logs, Traces의 역할과 차이를 이해한다.
- 장애 상황에서 어떤 데이터를 확인해야 하는지 판단하는 연습을 한다.
- Prometheus, Grafana, OpenTelemetry의 전체 흐름을 이해한다.
- 운영자, SRE, DevOps 관점에서 시스템을 바라보는 관점을 기른다.
- 학습 내용을 GitHub에 정리하고 발표를 통해 공유한다.
- 후반부에는 기본 데모 또는 개인 프로젝트에 Observability를 적용해본다.

---

## 4. 스터디 난이도

이 스터디는 Observability 개념을 기초부터 다루지만, 완전 입문반은 아닙니다.

스터디 중간중간 아래 개념이 함께 등장합니다.

- Linux
- Cloud
- Docker
- Kubernetes
- MSA
- Prometheus
- Grafana
- OpenTelemetry
- SRE / DevOps 운영 관점

Kubernetes나 Prometheus를 이미 잘 알고 있어야만 참여할 수 있는 것은 아닙니다. 다만 모르는 개념이 나왔을 때 스스로 찾아보고, 질문하고, 정리하려는 태도가 필요합니다.

---

## 5. 진행 방식

매주 정해진 책 범위를 읽고, 본인이 이해한 내용을 GitHub에 정리합니다.

세션에서는 당일 참석자 중 랜덤으로 발표자를 선정합니다. 발표자는 본인이 제출한 과제 내용을 바탕으로 약 5분 내외로 발표하고, 이후 Q&A와 토론을 진행합니다.

발표의 핵심은 책 내용을 완벽하게 요약하는 것이 아닙니다. 중요한 것은 이번 주 내용을 본인이 어떻게 이해했는지, 어떤 부분이 어려웠는지, 실제 운영 상황과 어떻게 연결할 수 있는지 공유하는 것입니다.

과제는 각 세션 전까지 제출하는 것을 권장합니다. 과제 미제출에 대한 별도 제재는 없지만, 제출 여부와 관계없이 세션 발표자로 선정될 수 있습니다.

---

## 6. 과제 작성 방식

과제는 매주 본인 브랜치에서 작성한 뒤 Pull Request로 제출합니다.

```text
members/{영문이름}/weekXX.md
```

과제 유형에 따라 아래 템플릿 중 하나를 참고합니다.

| 유형 | 템플릿 |
|---|---|
| 책 범위 정리 | `templates/assignment-template-book-summary.md` |
| 딥다이브 주제 정리 | `templates/assignment-template-deep-dive.md` |
| 실습 기록 | `templates/practice-template.md` |

과제에는 단순 요약뿐 아니라 아래 내용 중 하나 이상을 포함하는 것을 권장합니다.

- 본인이 중요하다고 생각한 개념
- 이해가 어려웠던 개념이나 용어
- 추가로 찾아본 예시
- 실제 운영 또는 프로젝트 경험과 연결되는 부분
- 장애 상황에서 어떤 데이터를 볼지에 대한 생각
- 함께 이야기해보고 싶은 질문

브랜치명, 파일명, PR 제목, commit message 등 제출 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)에 정리되어 있습니다.

---

## 7. 실습 방향

후반부에는 실습을 포함합니다. 실습은 전원이 동일한 고난도 환경을 구성하는 방식이 아니라, 각자의 상황에 맞게 **Base** 또는 **Project** 방향을 선택하는 방식으로 진행합니다.

### Base 방향

책 예제나 기본 데모를 따라가며 Prometheus, Grafana, Observability 도구의 흐름을 이해합니다.

예시:

- Prometheus 기본 구성 이해
- Grafana Dashboard 확인
- Exporter를 통한 Metrics 수집
- 간단한 장애 상황 가정 후 지표 확인
- 실행 과정, 오류, 해결 과정 정리

### Project 방향

개인 프로젝트 또는 공동 프로젝트에 Observability를 적용하는 방향입니다.

예시:

- 프로젝트 구조 정리
- 수집할 Metrics, Logs, Traces 정의
- Prometheus/Grafana 적용 방향 설계
- Dashboard 구성
- 장애 또는 부하 상황 가정
- 어떤 데이터를 보고 판단할 수 있는지 정리

실습 내용은 별도 파일명이 아니라 해당 주차 파일에 작성합니다. 예를 들어 6주차 실습은 `members/{영문이름}/week06.md`, 7주차 실습은 `members/{영문이름}/week07.md`에 작성합니다.

---

## 8. 커리큘럼

| 주차 | 주제 | 주요 내용 |
|---|---|---|
| 1주차 | 오리엔테이션 | 스터디 목적, 운영 방식, 과제/발표 방식, 자기소개 |
| 2주차 | 모니터링과 Observability 개념 이해 | Observability 필요성, Monitoring과 Observability 차이, Metrics/Logs/Traces |
| 3주차 | Observability 기반 기술 학습 | 트래픽 관리, 관측 가능성 프로세스, MSA, Kubernetes 관련 개념 |
| 4주차 | Prometheus | Prometheus 구조, 시계열 데이터, Exporter, Target, Label, PromQL |
| 5주차 | Grafana / LGTM Stack | Dashboard, Panel, Data Source, Alert, Loki, Mimir, Tempo |
| 6주차 | 데모 실습 진행 1 | Base 실습 또는 Project 적용 계획 수립 |
| 7주차 | 데모 실습 진행 2 | 실습 결과 정리, Dashboard 구성, 장애 상황 가정 |
| 8주차 | 산출물 공유 및 회고 | 최종 발표, GitHub 정리, 회고, 마무리 |

---

## 9. 레포지토리 구조

```text
09th-observability-mastery/
  README.md
  CONTRIBUTING.md
  .gitignore

  templates/
    assignment-template-book-summary.md
    assignment-template-deep-dive.md
    practice-template.md

  sessions/
    week01-ot.md
    week02-monitoring-observability.md

  members/
    Junwoo_Park/
      README.md
      week01.md
      week02.md

  .github/
    PULL_REQUEST_TEMPLATE.md
```

| 경로 | 설명 |
|---|---|
| `README.md` | 스터디 소개 및 전체 운영 요약 |
| `CONTRIBUTING.md` | 브랜치 생성, 과제 제출, PR 규칙 안내 |
| `templates/` | 과제와 실습 템플릿 |
| `sessions/` | 주차별 세션 요약 |
| `members/` | 참여자별 과제 제출 공간 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 작성 템플릿 |

---

## 10. 운영 철학

이 스터디는 각자의 경험과 이해도에 맞춰 함께 배워가는 방식으로 운영합니다.
모든 내용을 한 번에 완벽히 이해하기보다, 매주 조금씩 정리하고 질문을 나누는 과정을 중요하게 생각합니다.

스터디장은 학습 방향을 안내하고, 참여자들이 서로의 생각을 공유할 수 있는 흐름을 만드는 역할을 합니다.

참여자는 매주 학습한 내용을 본인의 언어로 정리하고, 어려웠던 부분이나 궁금한 점을 함께 나누면서 Observability를 운영 관점에서 이해해가는 것을 목표로 합니다.


---

## 11. 참고

- 주 교재: 『모니터링의 새로운 미래 관측 가능성』
- 주요 키워드: Observability, Monitoring, Metrics, Logs, Traces, Prometheus, Grafana, OpenTelemetry, Kubernetes, SRE, DevOps
