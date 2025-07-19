# 🚀 Reindeer 빠른 시작 가이드

## 📦 1. 환경 설정 (2분)

```bash
# 1. 저장소 클론
git clone <repository-url>
cd reindeer

# 2. 개발 환경 자동 설정
make dev-setup
```

## 🔧 2. 환경변수 설정 (1분)

```bash
# 환경변수 파일 복사
cp env.example .env

# .env 파일 수정 (최소 필수 설정)
nano .env
```

**최소 필수 환경변수:**

```bash
# PostgreSQL 설정
DB_HOST=localhost
DB_PORT=5432
DB_NAME=reindeer_dev
DB_USER=your_username
DB_PASSWORD=your_password

# 네이버 쇼핑 API (필수)
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret

# AWS S3 설정
S3_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## 🗄️ 3. 데이터베이스 준비 (2분)

```bash
# PostgreSQL 설치 (Mac)
brew install postgresql
brew services start postgresql

# 데이터베이스 생성
createdb reindeer_dev

# 또는 Docker로 실행
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

## 🏃‍♂️ 4. 서버 실행 (1분)

```bash
# 개발 서버 시작
make run

# 또는 직접 실행
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

## ✅ 5. 테스트

```bash
# API 테스트
curl "http://localhost:8000/api/v1/products/search?query=아이폰"

# API 문서 확인
open http://localhost:8000/docs
```

---

## 🛠️ 개발 명령어 모음

```bash
# 도움말 보기
make help

# 코드 포맷팅
make format

# 테스트 실행
make test

# 모든 검사 실행
make check

# 의존성 추가
make deps-add PACKAGE=requests
```

## 📚 추가 참고 문서

- [📋 개발 컨벤션](DEVELOPMENT_CONVENTIONS.md) - 코딩 스타일, 커밋 규칙 등
- [📖 README](README.md) - 프로젝트 전체 개요
- [🏗️ 아키텍처](docs/architecture.md) - 시스템 아키텍처 설명

## 🆘 문제 해결

### 자주 발생하는 문제들

**1. PostgreSQL 연결 오류**

```bash
# PostgreSQL 서비스 상태 확인
brew services list | grep postgresql

# 서비스 재시작
brew services restart postgresql
```

**2. 환경변수 로드 안됨**

```bash
# .env 파일 위치 확인
ls -la .env

# 환경변수 확인
python -c "import os; print(os.getenv('NAVER_CLIENT_ID'))"
```

**3. 의존성 설치 문제**

```bash
# uv 재설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 캐시 클리어 후 재설치
uv cache clean
uv sync
```

**4. 포트 이미 사용 중**

```bash
# 8000번 포트 사용하는 프로세스 확인
lsof -ti:8000

# 프로세스 종료
kill -9 $(lsof -ti:8000)
```

## 🎯 다음 단계

1. **첫 번째 API 호출 성공** ✅
2. [개발 컨벤션](DEVELOPMENT_CONVENTIONS.md) 읽기 📖
3. 첫 번째 브랜치 생성하고 기능 개발 시작 🌿
4. 첫 번째 PR 생성하기 🔄

---

**문제가 있으면 언제든 문의하세요!** 🙋‍♂️
