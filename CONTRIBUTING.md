# 과제 제출 가이드

이 문서는 **“모니터링 정복: Zero부터 시작하는 Observability”** 스터디의 GitHub 과제 제출 방법을 안내합니다.

목표는 Git 사용법을 완벽하게 익히는 것이 아니라, 매주 같은 흐름으로 학습 내용을 정리하고 Pull Request로 공유하는 것입니다.

---

## 1. 먼저 확인할 것

아래 규칙만 지키면 대부분의 제출 문제를 피할 수 있습니다.

1. `main` 브랜치에는 직접 수정하거나 push하지 않습니다.
2. 각자 본인 이름으로 브랜치를 생성합니다. 예: `Junwoo_Park`
3. 본인 폴더만 수정합니다. 예: `members/Junwoo_Park/`
4. 과제 파일은 `members/{영문이름}/weekXX.md` 형식으로 작성합니다.
5. Pull Request는 본인 브랜치에서 `main` 브랜치로 생성합니다.
6. 과제는 각 세션 전까지 제출하는 것을 권장합니다.
7. 과제 미제출에 대한 별도 제재는 없지만, 제출 여부와 관계없이 발표자로 선정될 수 있습니다.

실습 주차도 같은 파일명 규칙을 사용합니다. 예를 들어 6주차 실습은 `members/Junwoo_Park/week06.md`, 7주차 실습은 `members/Junwoo_Park/week07.md`에 작성합니다.

---

## 2. 이름과 위치 규칙

| 항목 | 규칙 | 예시 |
|---|---|---|
| 브랜치명 | `영문이름_영문성` | `Junwoo_Park` |
| 개인 폴더 | `members/{영문이름}/` | `members/Junwoo_Park/` |
| 개인 README | `members/{영문이름}/README.md` | `members/Junwoo_Park/README.md` |
| 주차 과제 | `members/{영문이름}/weekXX.md` | `members/Junwoo_Park/week02.md` |
| 실습 기록 | 해당 주차의 `weekXX.md` | `members/Junwoo_Park/week06.md` |
| PR 제목 | `[WeekXX] 이름 - 과제 주제` | `[Week02] 박준우 - Monitoring vs Observability 정리` |

브랜치명과 폴더명은 가능하면 동일하게 맞춥니다.

좋은 예시:

```text
Junwoo_Park
Taeyoung_Kim
Eunseo_Park
```

피해야 할 예시:

```text
박준우
junwoo park
Junwoo-Park!!!
```

---

## 3. 템플릿 선택

과제 유형에 따라 아래 템플릿 중 하나를 복사해서 작성합니다.

| 유형 | 템플릿 | 작성 위치 |
|---|---|---|
| 책 범위 정리 | `templates/assignment-template-book-summary.md` | `members/{영문이름}/weekXX.md` |
| 딥다이브 주제 정리 | `templates/assignment-template-deep-dive.md` | `members/{영문이름}/weekXX.md` |
| 실습 기록 | `templates/practice-template.md` | `members/{영문이름}/week06.md`, `week07.md` |

과제의 핵심은 글을 길게 쓰는 것이 아닙니다. 이번 주 내용을 **본인의 언어로 정리하고, 세션에서 함께 이야기할 질문이나 관점**을 남기는 것입니다.

---

## 4. 제출 흐름

매주 아래 순서로 진행합니다.

```text
1. main 브랜치 최신 상태 확인
2. 본인 브랜치로 이동
3. 템플릿을 members/{영문이름}/weekXX.md로 복사
4. 과제 작성
5. commit
6. push
7. Pull Request 생성
```

아래 runbook에서 `Junwoo_Park`, `week02.md`, commit message만 본인 상황에 맞게 바꿔 사용하면 됩니다.

---

## 5. Runbook: 처음 제출

예시: `Junwoo_Park`이 2주차 책 범위 정리 과제를 제출하는 경우

```bash
git clone https://github.com/cloud-club/09th-observability-mastery.git
cd 09th-observability-mastery

git checkout -b Junwoo_Park
mkdir -p members/Junwoo_Park

cp templates/assignment-template-book-summary.md members/Junwoo_Park/week02.md
```

`members/Junwoo_Park/week02.md` 파일을 작성한 뒤 제출합니다.

```bash
git status
git add members/Junwoo_Park/week02.md
git commit -m "docs: add week02 assignment - Junwoo_Park"
git push -u origin Junwoo_Park
```

GitHub 레포지토리 페이지에서 `Compare & pull request`를 클릭해 PR을 생성합니다.

PR 제목 예시:

```text
[Week02] 박준우 - Monitoring vs Observability 정리
```

---

## 6. Runbook: 다음 주차 제출

개인 브랜치는 계속 재사용합니다.

예시: 같은 참여자가 3주차 딥다이브 과제를 제출하는 경우

```bash
git checkout main
git pull origin main

git checkout Junwoo_Park
git merge main

cp templates/assignment-template-deep-dive.md members/Junwoo_Park/week03.md
```

`members/Junwoo_Park/week03.md` 파일을 작성한 뒤 제출합니다.

```bash
git status
git add members/Junwoo_Park/week03.md
git commit -m "docs: add week03 deep dive - Junwoo_Park"
git push origin Junwoo_Park
```

GitHub에서 새 Pull Request를 생성합니다.

---

## 7. Runbook: 실습 주차 제출

실습 주차에도 파일명은 `weekXX.md`를 사용합니다. 별도의 `practice.md` 파일을 만들지 않습니다.

예시: 6주차 실습 제출

```bash
git checkout main
git pull origin main

git checkout Junwoo_Park
git merge main

cp templates/practice-template.md members/Junwoo_Park/week06.md
```

`members/Junwoo_Park/week06.md` 파일을 작성한 뒤 제출합니다.

```bash
git status
git add members/Junwoo_Park/week06.md
git commit -m "docs: add week06 practice - Junwoo_Park"
git push origin Junwoo_Park
```

---

## 8. PR 생성 전 체크리스트

- [ ] 현재 브랜치가 `main`이 아니라 본인 브랜치인가?
- [ ] 과제 파일이 `members/{영문이름}/weekXX.md` 위치에 있는가?
- [ ] 실습 기록도 해당 주차의 `weekXX.md`에 작성했는가?
- [ ] 책 범위 정리 또는 딥다이브 템플릿 중 하나를 참고했는가?
- [ ] PR 방향이 `base: main`, `compare: 본인 브랜치`인가?
- [ ] PR 제목이 `[WeekXX] 이름 - 과제 주제` 형식인가?
- [ ] 다른 사람의 폴더를 수정하지 않았는가?

---

## 9. PR 생성 후 수정

PR을 만든 뒤에도 같은 브랜치에 다시 commit, push하면 기존 PR에 자동으로 반영됩니다. PR을 새로 만들 필요는 없습니다.

```bash
git add members/Junwoo_Park/week02.md
git commit -m "docs: update week02 assignment - Junwoo_Park"
git push origin Junwoo_Park
```

---

## 10. Commit Message 예시

| 상황 | Commit Message 예시 |
|---|---|
| 개인 README 추가 | `docs: add personal README - Junwoo_Park` |
| 주차 과제 추가 | `docs: add week02 assignment - Junwoo_Park` |
| 딥다이브 과제 추가 | `docs: add week03 deep dive - Junwoo_Park` |
| 실습 기록 추가 | `docs: add week06 practice - Junwoo_Park` |
| 과제 수정 | `docs: update week02 assignment - Junwoo_Park` |
| 오타 수정 | `docs: fix typo in week02 - Junwoo_Park` |

---

## 11. GitHub 웹 화면에서 제출하는 경우

Git 명령어 대신 GitHub 웹 화면에서 직접 제출해도 됩니다.

1. 레포지토리 상단의 브랜치 선택 버튼에서 본인 브랜치를 생성합니다.
2. `members/` 폴더에서 `Add file` → `Create new file`을 선택합니다.
3. 파일 경로를 `members/Junwoo_Park/week02.md`처럼 입력합니다.
4. 템플릿 내용을 복사해 작성한 뒤 commit합니다.
5. `Compare & pull request`를 클릭해 PR을 생성합니다.

웹 화면으로 제출해도 파일 위치, 파일명, PR 제목 규칙은 동일합니다.

---

## 12. 도움이 필요한 경우

GitHub 사용 중 막히는 부분이 있으면 Discord 채널에 질문합니다.

아래 정보를 함께 남겨주면 확인이 쉽습니다.

```text
1. 어떤 작업을 하려고 했는지
2. 어디에서 막혔는지
3. 에러 메시지 또는 화면 캡처
4. 사용한 브랜치명
5. 수정하려던 파일 경로
```
