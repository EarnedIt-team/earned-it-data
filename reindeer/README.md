# Reindeer - 제품 검색 및 이미지 처리 API

## 개요

이 프로젝트는 헥사고날 아키텍처를 기반으로 구축된 제품 검색 및 이미지 처리 시스템입니다.

## 주요 기능

- 네이버 쇼핑 API를 통한 제품 검색
- 이미지 자동 저장 (AWS S3)
- 이미지 배경 제거 기능
- 제품 정보 캐싱 (PostgreSQL)
- 비동기 처리 및 배치 작업 지원
- RESTful API 제공

## 기술 스택

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL (with asyncpg)
- **Storage**: AWS S3
- **HTTP Client**: aiohttp
- **Package Manager**: uv
- **DI Container**: dependency-injector

## 프로젝트 구조

```
reindeer/
├── app/                          # FastAPI 애플리케이션
│   ├── app.py                   # 메인 API 서버
│   ├── dto/                     # DTO 클래스들
│   │   ├── __init__.py
│   │   └── product_dto.py       # 제품 DTO
│   └── router/                  # API 라우터
│       ├── __init__.py
│       └── product_router.py    # 제품 라우터
├── browser/                     # 비즈니스 로직
│   ├── core/                    # 핵심 도메인
│   │   ├── entity/             # 엔터티
│   │   │   └── product.py      # 제품 엔터티
│   │   ├── infra/              # 인프라 클라이언트
│   │   │   ├── mysql_client.py
│   │   │   ├── naver_client.py
│   │   │   ├── postgresql_client.py
│   │   │   └── s3_client.py
│   │   ├── port/               # 포트 (인터페이스)
│   │   │   ├── product_fetcher.py
│   │   │   ├── product_repository.py
│   │   │   └── image_repository.py
│   │   └── usecase/            # 유스케이스
│   │       └── search_product.py
│   ├── adapter/                # 어댑터 (구현체)
│   │   ├── product_fetcher/
│   │   │   └── naver_fetcher.py # 네이버 API 클라이언트
│   │   └── repository/
│   │       ├── postgresql_repository.py # PostgreSQL 구현체
│   │       └── s3_repository.py    # S3 구현체
│   ├── di/                     # 의존성 주입
│   │   ├── base.py
│   │   └── config.py
│   └── task/                   # 태스크
│       └── search.py
├── pyproject.toml              # 의존성 관리
└── README.md                   # 이 파일
```

## 설치 및 실행

### 1. 의존성 설치

```bash
# uv 설치 (이미 설치되어 있지 않은 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 개발자 컴퓨터에서 환경 셋팅 필요 환경변수 등록 등등 gpt에게 물어보면 매우 잘해줌

# 의존성 설치
uv sync
```

### 2. 환경 변수 설정

`.env` 파일을 프로젝트 루트에 생성하고 내용을 추가하세요

### 3. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 연결 정보를 환경 변수에 설정하세요. 앱 실행 시 필요한 테이블이 자동으로 생성됩니다.

### 4. 애플리케이션 실행

```bash
# 개발 서버 실행
make run
```

## API 엔드포인트

### 기본 엔드포인트

- `GET /` - API 상태 확인
- `GET /health` - 시스템 상태 확인

### 제품 검색

- `GET /api/v1/products/search` - 제품 검색
  - **파라미터**:
    - `query` (string, required): 검색어
    - `use_cache` (boolean, optional): 캐시 사용 여부 (기본값: true)
    - `remove_background` (boolean, optional): 이미지 배경 제거 여부 (기본값: true)

#### 예시 요청

```bash
# 기본 검색
curl "http://localhost:8000/api/v1/products/search?query=아이폰%2014"

# 캐시 미사용 및 배경 제거 비활성화
curl "http://localhost:8000/api/v1/products/search?query=아이폰%2014&use_cache=false&remove_background=false"
```

#### 응답 예시

```json
{
  "products": [
    {
      "id": "88646679621",
      "name": "아이폰 14 256GB Apple 미개봉 새상품",
      "price": 447000.0,
      "image_url": "https://shopping-phinf.pstatic.net/main_8864667/88646679621.jpg",
      "url": "https://smartstore.naver.com/main/products/11102169299",
      "mall_name": "모바일 익스프레스",
      "product_type": "2",
      "maker": "Apple",
      "categories": ["디지털/가전", "휴대폰", "자급제폰"]
    }
  ],
  "total_count": 1,
  "query": "아이폰 14",
  "use_cache": true,
  "remove_background": true
}
```

## 최적화 특징

### 1. 성능 최적화

- **비동기 처리**: 모든 I/O 작업을 비동기로 처리
- **배치 처리**: 여러 제품을 한 번에 저장
- **연결 풀**: 데이터베이스 연결 풀 사용
- **병렬 처리**: 동시 검색 및 저장 지원
- **의존성 주입**: dependency-injector를 통한 효율적인 리소스 관리

### 2. 에러 처리

- **견고한 에러 핸들링**: 개별 제품 파싱 실패 시에도 계속 진행
- **타임아웃 설정**: HTTP 요청 타임아웃 설정
- **자동 재시도**: 실패한 요청 자동 재시도
- **상세한 오류 메시지**: 클라이언트에게 명확한 오류 정보 제공

### 3. 데이터 정제

- **HTML 태그 제거**: 네이버 API 응답의 HTML 태그 자동 제거
- **가격 파싱**: 문자열 가격을 숫자로 안전하게 변환
- **카테고리 추출**: 동적 카테고리 정보 추출

### 4. 캐싱 및 저장

- **제품 정보 캐싱**: 검색 결과를 PostgreSQL에 캐시
- **이미지 처리**: S3에 이미지 자동 저장 및 중복 방지
- **배경 제거**: 이미지 배경 제거 기능 (선택적)

## 개발 도구

### 코드 포맷팅

```bash
# 코드 포맷팅
uv run black .
uv run isort .

# 타입 체크
uv run mypy .

# 린팅
uv run flake8 .
```

### 테스트

```bash
# 테스트 실행
uv run pytest

# 배경 제거 테스트
uv run python test_background_removal.py
```

## 배포

1. 환경 변수 설정
2. PostgreSQL 데이터베이스 연결 확인
3. AWS S3 권한 설정
4. 네이버 API 키 설정
5. 프로덕션 서버 실행

## 아키텍처 특징

### 헥사고날 아키텍처

- **Port**: 비즈니스 로직에서 외부 시스템과의 인터페이스 정의
- **Adapter**: Port의 구현체로 실제 외부 시스템과 통신
- **Entity**: 비즈니스 엔터티 정의
- **UseCase**: 비즈니스 로직 구현

### 의존성 주입

- **BaseContainer**: 모든 의존성을 관리하는 중앙 컨테이너
- **Config**: 설정 관리
- **Resource Management**: 리소스 초기화 및 정리 자동화

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!
