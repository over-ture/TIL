# git 사용법
1. git bash에서 디렉토리 이동 후 `git init`으로 로컬 저장소 생성
2. `git add 'file'` 사용하여 스테이지에 파일 추가
3. `git commit` 사용하여 변경 사항 커밋

## github 리포지토리에 Push
1. github에서 repository 생성
2. 해당 리포지토리로 
```bash
`git remote add origin '리포지토리 주소.git'`
```
3. ```bash
    `git push origin '브랜치 이름'`
    ``` 
    을 사용하여 github에 Push

## 브랜치 생성 및 선택
1. 브랜치 생성:

브랜치를 생성하기 위해 git branch 명령을 사용합니다. 예를 들어, `feature-x`라는 이름의 브랜치를 생성하려면 다음과 같이 입력합니다:
```bash
- git branch feature-x
```

2. 브랜치 선택(체크아웃):

브랜치를 선택하려면 git checkout 명령을 사용합니다. `feature-x`브랜치로 전환하려면 다음과 같이 입력합니다:
```bash
git checkout feature-x
```

3. 브랜치 생성 및 선택을 동시에 하기:

새로운 브랜치를 생성하면서 동시에 그 브랜치로 전환하려면 -b 옵션을 사용하여 git checkout 명령을 실행합니다:
```bash
git checkout -b feature-x
```

이 명령은 `feature-x`라는 브랜치를 생성하고, 그 브랜치로 바로 전환합니다.

4. 현재 선택된 브랜치 확인:

현재 어떤 브랜치가 선택되어 있는지 확인하려면 git branch 명령만 실행하면 됩니다: 
```bash
git branch
```

이 명령을 실행하면 모든 브랜치의 목록이 표시되며, 현재 선택된 브랜치 앞에 `*` 표시가 있습니다.