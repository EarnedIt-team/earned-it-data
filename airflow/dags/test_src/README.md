# 다나와 크롤링 프로젝트

다나와 온라인 쇼핑몰에서 카테고리별 상품 정보를 크롤링하는 프로젝트입니다.

## 주요 기능

### 🆕 새로운 기능: 사이드바 카테고리 동적 크롤링

- **다나와 홈페이지 사이드바 카테고리 자동 수집**: 홈페이지의 사이드바에서 실시간으로 카테고리 URL을 수집합니다.
- **AI 카테고리 자동 제외**: AI 관련 카테고리는 자동으로 제외됩니다.
- **동적 카테고리 URL 생성**: 수집된 카테고리 정보를 바탕으로 크롤링 URL을 자동 생성합니다.

### 기존 기능

- **전체 카테고리 크롤링**: 다나와의 모든 주요 카테고리를 크롤링합니다.
- **상품 정보 수집**: 상품명, 가격, 이미지, URL 등 상세 정보를 수집합니다.
- **중복 제거**: 동일한 상품의 중복 수집을 방지합니다.
- **오류 처리**: 크롤링 중 발생하는 오류를 처리하고 로그를 기록합니다.

## 사용법

### 환경 변수 설정

```bash
# 기본 설정
export MAX_PAGES_PER_CATEGORY=3          # 카테고리당 최대 페이지 수
export USE_DYNAMIC_CATEGORIES=true       # 동적 카테고리 수집 사용 여부
export USE_SIDEBAR_CRAWLING=true         # 사이드바 카테고리 크롤링 사용 여부
```

### 실행 방법

#### 1. 사이드바 카테고리 크롤링 (권장)

```bash
# 다나와 홈페이지 사이드바에서 카테고리를 동적으로 수집하여 크롤링
export USE_SIDEBAR_CRAWLING=true
export USE_DYNAMIC_CATEGORIES=true
python main.py
```

#### 2. 전체 카테고리 크롤링 (동적 수집)

```bash
# 동적 카테고리 수집을 사용하되, 전체 카테고리 크롤링 모드
export USE_SIDEBAR_CRAWLING=false
export USE_DYNAMIC_CATEGORIES=true
python main.py
```

#### 3. 전체 카테고리 크롤링 (기본 목록)

```bash
# 하드코딩된 카테고리 목록을 사용
export USE_SIDEBAR_CRAWLING=false
export USE_DYNAMIC_CATEGORIES=false
python main.py
```

### 테스트 실행

```bash
# 사이드바 카테고리 크롤링 기능 테스트
python test_sidebar_crawling.py
```

## 크롤링 모드 비교

| 모드             | 카테고리 수집 방식                             | 장점                                      | 단점                    |
| ---------------- | ---------------------------------------------- | ----------------------------------------- | ----------------------- |
| 사이드바 크롤링  | 홈페이지 사이드바에서 실시간 수집              | 최신 카테고리 반영, AI 카테고리 자동 제외 | 약간의 추가 시간 소요   |
| 동적 전체 크롤링 | 홈페이지에서 동적 수집 + 하드코딩 서브카테고리 | 포괄적인 크롤링                           | 복잡한 구조             |
| 기본 전체 크롤링 | 하드코딩된 카테고리 목록                       | 빠른 실행                                 | 최신 카테고리 반영 불가 |

## 프로젝트 구조

```
danawa_crawling/
├── main.py                    # 메인 실행 파일
├── test_sidebar_crawling.py   # 사이드바 크롤링 테스트
├── src/
│   ├── __init__.py
│   ├── crawler.py            # 크롤러 메인 클래스
│   ├── categories.py         # 카테고리 정보 및 동적 수집 함수
│   ├── models.py             # 데이터 모델
│   └── utils.py              # 유틸리티 함수
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 주요 클래스 및 함수

### DanawaCrawler 클래스

- `crawl_all_categories()`: 전체 카테고리 크롤링
- `crawl_sidebar_categories()`: 사이드바 카테고리 크롤링 (신규)
- `crawl_category()`: 단일 카테고리 크롤링
- `get_statistics()`: 크롤링 통계 정보 반환

### 카테고리 수집 함수

- `get_sidebar_categories()`: 사이드바 카테고리 동적 수집 (신규)
- `get_dynamic_category_urls()`: 동적 카테고리 URL 생성 (신규)
- `get_category_urls()`: 기본 카테고리 URL 목록
- `get_default_categories()`: 백업용 기본 카테고리 (신규)

## AI 카테고리 제외 기능

다음 키워드가 포함된 카테고리는 자동으로 제외됩니다:

- "AI" (대소문자 구분 없음)
- "인공지능"

## 출력 파일 형식

크롤링 결과는 JSON 형태로 저장됩니다:

```json
{
  "crawling_info": {
    "timestamp": "20231201_143000",
    "total_categories": 10,
    "total_products": 1500
  },
  "categories": {
    "가전·TV_전체": {
      "summary": {
        "category": "가전·TV > 전체",
        "total_products": 150,
        "successful_products": 148,
        "failed_products": 2
      },
      "products": [
        {
          "product_id": "12345",
          "name": "삼성 QLED TV",
          "category": "가전·TV",
          "price": 1500000,
          "image_url": "https://...",
          "product_url": "https://...",
          "crawled_at": "2023-12-01T14:30:00"
        }
      ]
    }
  }
}
```

## 의존성

- Python 3.8+
- selenium
- webdriver-manager
- requests
- beautifulsoup4

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 또는 poetry 사용
poetry install

# 실행
python main.py

# 테스트
python test_sidebar_crawling.py
```

## 주의사항

- 크롤링 시 서버 부하를 방지하기 위해 페이지 간 딜레이가 적용됩니다.
- Chrome 브라우저와 ChromeDriver가 필요합니다.
- 다나와 사이트 구조 변경 시 셀렉터 수정이 필요할 수 있습니다.
- AI 카테고리 제외 기능은 카테고리명을 기준으로 합니다.

## 로그 예시

```
🚀 다나와 사이드바 카테고리 크롤링 시작!
📡 다나와 홈페이지 사이드바에서 동적 카테고리 수집 중...
🔍 다나와 홈페이지 사이드바 카테고리 수집 시작...
✅ 선택자 '.category_menu .category_item'로 12개 카테고리 발견
✅ 카테고리 수집: 가전·TV
⚠️ AI 카테고리 제외: AI 전자제품
✅ 동적 카테고리 수집 완료
📊 수집된 사이드바 카테고리: 10개
🗂️ 사이드바 카테고리:
  1. 가전·TV
  2. 컴퓨터·노트북
  3. 태블릿·모바일
  ...
[1/10] 🔍 '가전·TV' 크롤링 중...
✅ 완료: 45개 상품 수집
🎉 사이드바 카테고리 크롤링 완료!
```
