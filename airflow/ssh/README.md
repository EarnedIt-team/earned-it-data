# SSH 키 설정 가이드

이 폴더는 GitHub에서 DAGs를 자동으로 동기화하기 위한 SSH 키를 저장하는 곳입니다.

## 1. SSH 키 생성

```bash
# SSH 키 생성 (GitHub 계정 이메일 사용)
ssh-keygen -t rsa -b 4096 -C "youngchannel4u@gmail.com" -f ./ssh/id_rsa

# 키 권한 설정
chmod 600 ./ssh/id_rsa
chmod 644 ./ssh/id_rsa.pub
chmod 700 ./ssh
```

## 2. GitHub에 공개 키 등록

1. 공개 키 내용 확인:

   ```bash
   cat ./ssh/id_rsa.pub
   ```

2. GitHub 설정:
   - GitHub → Settings → SSH and GPG keys
   - "New SSH key" 클릭
   - 공개 키 내용 붙여넣기
   - "Add SSH key" 클릭

## 3. Git 저장소 URL 설정

`.env` 파일에서 HTTPS 대신 SSH URL 사용:

```bash
# HTTPS (Personal Access Token 필요)
GIT_SYNC_REPO=https://github.com/username/repo.git

# SSH (권장)
GIT_SYNC_REPO=git@github.com:username/repo.git
```

## 4. Personal Access Token 방식 (대안)

SSH 키 대신 Personal Access Token 사용 가능:

1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" 클릭
3. `repo` 권한 선택
4. `.env` 파일에 설정:
   ```bash
   GIT_SYNC_REPO=https://your-token@github.com/username/repo.git
   ```

## 보안 주의사항

- 이 폴더의 파일들은 `.gitignore`에 포함되어야 합니다
- SSH 키는 절대 공개 저장소에 업로드하지 마세요
- 정기적으로 키를 갱신하세요
