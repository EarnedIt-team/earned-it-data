# Reindeer 개발 컨벤션

## 📋 목차

1. [코드 스타일](#-코드-스타일)
2. [네이밍 컨벤션](#-네이밍-컨벤션)
3. [프로젝트 구조](#-프로젝트-구조)
4. [커밋 메시지 규칙](#-커밋-메시지-규칙)
5. [브랜치 전략](#-브랜치-전략)
6. [코드 리뷰 가이드라인](#-코드-리뷰-가이드라인)
7. [테스트 규칙](#-테스트-규칙)
8. [문서화 규칙](#-문서화-규칙)
9. [개발 워크플로우](#-개발-워크플로우)

---

## 🎨 코드 스타일

### Python 코드 스타일

- **PEP 8** 준수 (Black으로 자동 포맷팅)
- **줄 길이**: 최대 88자 (Black 기본값)
- **인덴트**: 공백 4칸
- **문자열**: 가능하면 double quotes (`"`) 사용

```python
# ✅ 좋은 예
async def search_product(
    query: str,
    use_cache: bool = True,
    remove_background: bool = True
) -> List[Product]:
    """제품을 검색합니다."""
    pass

# ❌ 나쁜 예
async def search_product(query:str,use_cache:bool=True,remove_background:bool=True)->List[Product]:
    pass
```

### Import 순서 (isort 적용)

1. 표준 라이브러리
2. 서드파티 라이브러리
3. 로컬 애플리케이션/라이브러리

```python
# 1. 표준 라이브러리
import asyncio
import logging
from typing import List, Optional

# 2. 서드파티 라이브러리
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 3. 로컬 애플리케이션
from browser.core.entity.product import Product
from browser.core.usecase.search_product import SearchProduct
```

### 타입 힌트

- **모든 함수**에 타입 힌트 필수 적용
- **클래스 속성**에도 타입 힌트 적용
- `mypy` strict 모드 준수

```python
# ✅ 좋은 예
from typing import List, Optional

async def fetch_products(query: str, limit: int = 10) -> List[Product]:
    """제품을 가져옵니다."""
    pass

class ProductRepository:
    def __init__(self, connection_pool: asyncpg.Pool) -> None:
        self.connection_pool = connection_pool

# ❌ 나쁜 예
async def fetch_products(query, limit=10):
    pass
```

---

## 📝 네이밍 컨벤션

### 파일 및 디렉토리

- **파일명**: `snake_case.py`
- **디렉토리명**: `snake_case/`

```
✅ 좋은 예:
browser/core/usecase/search_product.py
app/dto/product_dto.py

❌ 나쁜 예:
browser/core/usecase/SearchProduct.py
app/dto/ProductDTO.py
```

### Python 네이밍

```python
# 클래스명: PascalCase
class ProductRepository:
    pass

class SearchProduct:
    pass

# 함수/메서드명: snake_case
async def search_product():
    pass

async def fetch_product_from_api():
    pass

# 변수명: snake_case
user_query = "아이폰"
product_list = []
is_cache_enabled = True

# 상수: SCREAMING_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRY_COUNT = 3
NAVER_BASE_URL = "https://openapi.naver.com"

# 비공개 메서드/속성: 앞에 언더스코어 1개
class NaverFetcher:
    def _clean_html_tags(self, text: str) -> str:
        pass

    def _parse_price(self, price_str: str) -> float:
        pass

# 매직 메서드: 앞뒤 언더스코어 2개
def __init__(self):
    pass
```

### API 엔드포인트

- **RESTful** 원칙 준수
- **복수형 명사** 사용
- **kebab-case** 사용 (필요시)

```python
# ✅ 좋은 예
@router.get("/api/v1/products/search")
@router.get("/api/v1/products/{product_id}")
@router.post("/api/v1/products")

# ❌ 나쁜 예
@router.get("/api/v1/product/search")
@router.get("/api/v1/searchProduct")
```

---

## 🏗️ 프로젝트 구조

### 디렉토리 구조 규칙

```
reindeer/
├── app/                          # FastAPI 애플리케이션 레이어
│   ├── app.py                   # 메인 애플리케이션
│   ├── dto/                     # DTO (Data Transfer Objects)
│   │   ├── __init__.py
│   │   └── {domain}_dto.py      # 도메인별 DTO
│   └── router/                  # API 라우터
│       ├── __init__.py
│       └── {domain}_router.py   # 도메인별 라우터
├── browser/                     # 비즈니스 로직 레이어
│   ├── core/                    # 핵심 비즈니스 로직
│   │   ├── entity/             # 도메인 엔터티
│   │   ├── port/               # 인터페이스 (포트)
│   │   ├── usecase/            # 유스케이스 (비즈니스 로직)
│   │   └── infra/              # 인프라 클라이언트
│   ├── adapter/                # 어댑터 (포트 구현체)
│   │   ├── repository/         # 저장소 구현체
│   │   └── {external_service}/ # 외부 서비스 구현체
│   ├── di/                     # 의존성 주입 설정
│   └── task/                   # 독립 실행 태스크
├── tests/                      # 테스트 코드
│   ├── unit/                   # 단위 테스트
│   ├── integration/            # 통합 테스트
│   └── fixtures/               # 테스트 픽스처
├── docs/                       # 문서
├── scripts/                    # 유틸리티 스크립트
└── pyproject.toml             # 프로젝트 설정
```

### 헥사고날 아키텍처 규칙

```python
# ✅ Port (인터페이스) - browser/core/port/
from abc import ABC, abstractmethod

class ProductRepository(ABC):
    @abstractmethod
    async def save_product(self, product: Product) -> None:
        pass

# ✅ Entity - browser/core/entity/
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    # ...

# ✅ UseCase - browser/core/usecase/
class SearchProduct:
    def __init__(
        self,
        product_fetcher: ProductFetcher,
        product_repository: ProductRepository
    ):
        # ...

# ✅ Adapter - browser/adapter/
class PostgreSQLRepository(ProductRepository):
    async def save_product(self, product: Product) -> None:
        # 구현
        pass
```

---

## 📢 커밋 메시지 규칙

### 커밋 메시지 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 종류

- **feat**: 새로운 기능
- **fix**: 버그 수정
- **docs**: 문서 수정
- **style**: 코드 포맷팅, 세미콜론 누락 등 (기능 변화 없음)
- **refactor**: 코드 리팩토링 (기능 변화 없음)
- **test**: 테스트 코드 추가/수정
- **chore**: 빌드 과정 또는 보조 도구 변경

### Scope 종류

- **api**: API 레이어 관련
- **core**: 비즈니스 로직 관련
- **infra**: 인프라 관련 (DB, 외부 API 등)
- **config**: 설정 관련
- **deps**: 의존성 관련

### 예시

```bash
# ✅ 좋은 예
feat(api): 제품 검색 API 엔드포인트 추가

네이버 쇼핑 API를 활용한 제품 검색 기능 구현
- GET /api/v1/products/search 엔드포인트 추가
- 검색어 유효성 검증 로직 포함
- 캐시 옵션과 배경 제거 옵션 지원

Closes #123

fix(core): 제품 가격 파싱 시 예외 처리 개선

가격 정보가 없는 경우 0.0으로 기본값 설정
- 빈 문자열이나 None 값 처리 추가
- 숫자가 아닌 문자 제거 로직 강화

docs(readme): API 사용 예시 추가

chore(deps): rembg 라이브러리 버전 업데이트

# ❌ 나쁜 예
fix bug
update code
add feature
```

### 커밋 메시지 작성 규칙

1. **제목은 50자 이내**
2. **제목은 명령조로** 작성 ("추가했다" X, "추가" O)
3. **제목 첫 글자는 소문자**
4. **제목 끝에 마침표 없음**
5. **본문과 제목 사이 빈 줄**
6. **본문은 72자에서 줄바꿈**
7. **"무엇을", "왜" 변경했는지 설명**

---

## 🌿 브랜치 전략

### 브랜치 네이밍

```bash
# 기능 개발
feat/{issue-number}-{brief-description}
feat/123-product-search-api

# 버그 수정
fix/{issue-number}-{brief-description}
fix/456-price-parsing-error

# 핫픽스
hotfix/{issue-number}-{brief-description}
hotfix/789-critical-security-fix

# 릴리즈
release/v{version}
release/v1.2.0

# 문서
docs/{topic}
docs/api-specification
```

### 브랜치 전략

- **main**: 프로덕션 코드
- **develop**: 개발 통합 브랜치
- **feature/\***: 기능 개발
- **fix/\***: 버그 수정
- **hotfix/\***: 긴급 수정
- **release/\***: 릴리즈 준비

### 워크플로우

1. `develop`에서 `feature/` 브랜치 생성
2. 기능 개발 완료 후 `develop`으로 PR
3. 코드 리뷰 후 머지
4. `release/` 브랜치에서 QA
5. `main`으로 머지 후 배포

---

## 👥 코드 리뷰 가이드라인

### PR 제목 및 설명

````markdown
## 변경 사항

- 제품 검색 API 엔드포인트 구현
- 네이버 쇼핑 API 연동 로직 추가

## 테스트 방법

```bash
curl "http://localhost:8000/api/v1/products/search?query=아이폰"
```
````

## 체크리스트

- [ ] 타입 힌트 적용
- [ ] 단위 테스트 작성
- [ ] 문서화 업데이트
- [ ] 에러 처리 구현

````

### 리뷰어 체크포인트

1. **아키텍처 준수**: 헥사고날 아키텍처 원칙 따름
2. **타입 안전성**: mypy 에러 없음
3. **테스트 커버리지**: 핵심 로직 테스트 작성
4. **에러 처리**: 예외 상황 적절히 처리
5. **성능**: 불필요한 동기 호출 없음
6. **보안**: 입력값 검증, SQL 인젝션 방지
7. **문서화**: docstring, 주석 적절히 작성

### 코드 리뷰 코멘트 예시

```python
# ✅ 건설적인 피드백
# 💡 제안: 이 부분을 async/await로 변경하면 성능이 향상될 것 같습니다.

# ⚠️ 문제: 이 함수에서 예외가 발생하면 전체 프로세스가 중단될 수 있습니다.

# ❓ 질문: 이 매직 넘버 100의 의미를 상수로 정의하는 게 어떨까요?

# ❌ 나쁜 예
# 이거 왜 이렇게 했나요?
# 잘못됐네요
````

---

## 🧪 테스트 규칙

### 테스트 구조

```
tests/
├── unit/                       # 단위 테스트
│   ├── core/
│   │   ├── test_search_product.py
│   │   └── test_product_entity.py
│   └── adapter/
│       └── test_naver_fetcher.py
├── integration/                # 통합 테스트
│   ├── test_api_endpoints.py
│   └── test_database_integration.py
├── fixtures/                   # 테스트 데이터
│   ├── product_samples.json
│   └── naver_api_response.json
└── conftest.py                # pytest 설정
```

### 테스트 네이밍

```python
# 테스트 함수명: test_{테스트대상}_{조건}_{예상결과}
def test_search_product_with_valid_query_returns_products():
    pass

def test_search_product_with_empty_query_raises_validation_error():
    pass

def test_fetch_product_with_api_error_returns_empty_list():
    pass

# 테스트 클래스명: Test{테스트대상}
class TestSearchProduct:
    def test_search_with_cache_enabled_returns_cached_result(self):
        pass

    def test_search_with_cache_disabled_calls_external_api(self):
        pass
```

### 테스트 작성 규칙

1. **AAA 패턴** (Arrange, Act, Assert)
2. **독립성**: 각 테스트는 서로 독립적
3. **명확성**: 테스트 의도가 명확히 드러남
4. **속도**: 빠른 실행을 위한 모킹 활용

```python
# ✅ 좋은 예
@pytest.mark.asyncio
async def test_search_product_with_valid_query_returns_products():
    # Arrange
    mock_fetcher = Mock()
    mock_repository = Mock()
    search_usecase = SearchProduct(mock_fetcher, mock_repository, None)

    expected_products = [Product(id="1", name="아이폰", price=100000.0)]
    mock_fetcher.fetch_product.return_value = expected_products

    # Act
    result = await search_usecase.search_product("아이폰")

    # Assert
    assert len(result) == 1
    assert result[0].name == "아이폰"
    mock_fetcher.fetch_product.assert_called_once_with("아이폰")
```

### 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest

# 특정 테스트 파일 실행
uv run pytest tests/unit/core/test_search_product.py

# 커버리지와 함께 실행
uv run pytest --cov=browser --cov=app

# 마커로 특정 테스트만 실행
uv run pytest -m "not integration"
```

---

## 📚 문서화 규칙

### Docstring 스타일 (Google Style)

```python
def search_product(
    query: str,
    use_cache: bool = True,
    remove_background: bool = True
) -> List[Product]:
    """제품을 검색합니다.

    네이버 쇼핑 API를 통해 제품 정보를 가져오고,
    선택적으로 캐시를 사용하고 이미지 배경을 제거합니다.

    Args:
        query: 검색할 제품명 또는 키워드
        use_cache: 캐시된 결과를 사용할지 여부
        remove_background: 제품 이미지의 배경을 제거할지 여부

    Returns:
        검색된 제품 객체들의 리스트. 검색 결과가 없으면 빈 리스트.

    Raises:
        ValueError: 검색어가 비어있거나 유효하지 않은 경우
        APIError: 외부 API 호출 실패 시

    Examples:
        >>> products = await search_product("아이폰 14")
        >>> print(f"Found {len(products)} products")
        Found 5 products

        >>> products = await search_product("아이폰", use_cache=False)
        >>> # 캐시를 사용하지 않고 직접 API 호출
    """
    pass
```

### 코드 주석 규칙

```python
# ✅ 좋은 주석 - "왜"를 설명
# 네이버 API는 HTML 태그를 포함해서 응답하므로 제거 필요
clean_name = self._clean_html_tags(raw_name)

# 배경 제거는 CPU 집약적이므로 executor에서 실행
output_image = await asyncio.get_event_loop().run_in_executor(
    None, remove, input_image
)

# ❌ 나쁜 주석 - "무엇"을 중복 설명
# 이름을 정리한다
clean_name = self._clean_html_tags(raw_name)

# i를 1 증가시킨다
i += 1
```

### API 문서화

FastAPI의 자동 문서 생성을 최대한 활용:

```python
@router.get(
    "/search",
    response_model=SearchResponse,
    summary="제품 검색",
    description="네이버 쇼핑 API를 통해 제품을 검색합니다.",
    response_description="검색된 제품 목록과 메타데이터",
    responses={
        200: {
            "description": "검색 성공",
            "content": {
                "application/json": {
                    "example": {
                        "products": [...],
                        "total_count": 10,
                        "query": "아이폰"
                    }
                }
            }
        },
        400: {"description": "잘못된 요청 파라미터"},
        503: {"description": "외부 서비스 이용 불가"}
    }
)
```

---

## ⚙️ 개발 워크플로우

### 개발 환경 설정

```bash
# 1. 저장소 클론
git clone <repository-url>
cd reindeer

# 2. Python 환경 설정
uv sync

# 3. 개발 도구 설정
uv run pre-commit install  # pre-commit 훅 설치

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 5. 데이터베이스 설정
# PostgreSQL 실행 및 데이터베이스 생성
```

### 개발 명령어

```bash
# 개발 서버 실행
make run
# 또는
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000

# 코드 포맷팅
uv run black .
uv run isort .

# 타입 체크
uv run mypy .

# 린팅
uv run flake8 .

# 테스트 실행
uv run pytest

# 모든 검사 한번에 실행
make check  # Makefile에 추가 예정
```

### Pre-commit 훅

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### 기능 개발 워크플로우

1. **이슈 생성** → GitHub Issues
2. **브랜치 생성** → `feat/123-feature-description`
3. **개발 진행**
   - 코드 작성
   - 테스트 작성
   - 문서 업데이트
4. **로컬 검증**
   - `make check` 실행
   - 모든 테스트 통과 확인
5. **PR 생성**
   - 템플릿에 따라 작성
   - 적절한 리뷰어 지정
6. **코드 리뷰**
   - 피드백 반영
   - 승인 받기
7. **머지** → `develop` 브랜치

### 릴리즈 워크플로우

1. **릴리즈 브랜치 생성** → `release/v1.2.0`
2. **QA 진행**
3. **버그 수정** (필요시)
4. **버전 태그 생성**
5. **main 브랜치 머지**
6. **배포 진행**

---

## 🔧 도구 설정

### pyproject.toml 추가 설정

```toml
[tool.black]
line-length = 88
target-version = ['py311']
extend-exclude = '''
/(
  # 제외할 디렉토리들
  \.eggs
  | \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]

[tool.coverage.run]
source = ["app", "browser"]
omit = ["tests/*", ".venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

이 컨벤션을 팀 전체가 따라주시면 코드의 일관성과 품질을 유지할 수 있습니다! 🚀
