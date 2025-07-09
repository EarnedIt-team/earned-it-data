# Airflow 단일 서버 설정

이 폴더에는 단일 서버에서 실행되는 Apache Airflow 설정이 포함되어 있습니다.

## 필요 사항

- Docker
- Docker Compose

## 설정 방법

1. **환경 변수 설정**

   ```bash
   cp env.example .env
   ```

2. **권한 설정**

   ```bash
   chmod +x start.sh
   ```

3. **Airflow 시작**
   ```bash
   ./start.sh
   ```

## Poetry 사용법

이 프로젝트는 Poetry를 사용하여 의존성을 관리합니다.

### 의존성 추가

```bash
poetry add <package-name>
```

### 개발 의존성 추가

```bash
poetry add --group dev <package-name>
```

### 의존성 제거

```bash
poetry remove <package-name>
```

### 의존성 설치

```bash
poetry install
```

**참고**: 의존성을 변경한 후에는 Docker 이미지를 다시 빌드해야 합니다:

```bash
docker-compose build
```

## 접속 정보

- **웹 UI**: http://localhost:8080
- **사용자명**: airflow
- **비밀번호**: airflow

## 유용한 명령어

### 상태 확인

```bash
docker-compose ps
```

### 로그 확인

```bash
docker-compose logs -f
```

### 특정 서비스 로그 확인

```bash
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

### 중지

```bash
docker-compose down
```

### 완전 정리 (데이터베이스 포함)

```bash
docker-compose down -v
```

## 폴더 구조

```
airflow/
├── docker-compose.yml      # Docker Compose 설정
├── pyproject.toml         # Poetry 의존성 설정
├── poetry.lock            # Poetry lock 파일
├── Dockerfile             # 커스텀 Docker 이미지
├── env.example            # 환경 변수 예제
├── start.sh               # 시작 스크립트
├── cleanup_logs.sh        # 로그 정리 스크립트
├── dags/                  # DAG 파일들
│   └── example_dag.py     # 예제 DAG
├── logs/                  # 로그 파일들
└── plugins/               # 플러그인 파일들
```

## 로그 관리 (서버 용량 절약)

이 설정은 서버 용량을 절약하기 위해 최소한의 로그 관리를 수행합니다:

### 자동 로그 관리 설정

- **로그 레벨**: WARNING (오류와 경고만 기록)
- **보관 기간**: 3일 (기본 30일에서 단축)
- **Docker 로그**: 파일당 최대 10MB, 최대 3개 파일만 유지

### 수동 로그 정리

```bash
./cleanup_logs.sh
```

이 스크립트는 다음 작업을 수행합니다:

- 3일 이상 된 로그 파일 삭제
- 빈 로그 디렉토리 정리
- Docker 시스템 정리
- 50MB 이상 로그 파일 압축

### 로그 디렉토리 크기 확인

```bash
du -sh logs/
```

## DAG 개발

- `dags/` 폴더에 Python 파일을 추가하면 자동으로 Airflow에서 인식됩니다.
- 파일을 수정하면 자동으로 반영됩니다.

## 트러블슈팅

### 권한 문제

macOS에서 권한 문제가 발생할 수 있습니다. 이 경우 `.env` 파일에서 `AIRFLOW_UID`를 현재 사용자 ID로 변경하세요:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 메모리 부족

최소 4GB의 메모리가 필요합니다. Docker Desktop에서 메모리 할당량을 확인하세요.

### 포트 충돌

8080 포트가 이미 사용 중이면 `docker-compose.yml`에서 포트를 변경하세요:

```yaml
ports:
  - "8081:8080" # 8081로 변경
```
