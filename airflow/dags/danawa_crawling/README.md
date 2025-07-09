# 다나와 크롤링 프로젝트

다나와 상품 정보를 크롤링하는 프로젝트입니다.

## 개발 환경 설정

### Poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 의존성 설치

```bash
poetry install
```

### 로컬 실행

```bash
poetry run python main.py
```

## Docker 실행

### 이미지 빌드

```bash
docker build -t danawa-crawling .
```

### 컨테이너 실행

```bash
docker run --rm danawa-crawling
```

## 프로젝트 구조

```
danawa_crawling/
├── main.py          # 메인 실행 파일
├── pyproject.toml   # Poetry 설정
├── Dockerfile       # Docker 설정
├── README.md        # 프로젝트 설명
├── core/           # 핵심 비즈니스 로직
├── usecase/        # 사용 사례
├── adapter/        # 어댑터
└── infra/          # 인프라 계층
```

## 개발 가이드

### 코드 포맷팅

```bash
poetry run black .
```

### 린트 검사

```bash
poetry run flake8 .
```

### 타입 검사

```bash
poetry run mypy .
```

### 테스트 실행

```bash
poetry run pytest
```
