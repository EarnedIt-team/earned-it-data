import aiohttp
import urllib.parse
import re
import logging
from typing import List
from browser.core.port.product_fetcher import ProductFetcher
from browser.core.entity.product import Product
from html import unescape

logger = logging.getLogger(__name__)


class NaverFetcher(ProductFetcher):
    def __init__(self, naver_client: aiohttp.ClientSession, client_id: str, client_secret: str):
        self.naver_client = naver_client
        self.client_id = client_id
        self.client_secret = client_secret
    
    def _clean_html_tags(self, text: str) -> str:
        """HTML 태그를 제거하고 HTML 엔티티를 디코딩합니다."""
        if not text:
            return ""
        
        text = re.sub(r'<[^>]+>', '', text)
        text = unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_categories(self, item: dict) -> List[str]:
        """카테고리 정보를 추출합니다."""
        categories = []
        for i in range(1, 5):
            category = item.get(f"category{i}")
            if category:
                categories.append(self._clean_html_tags(category))
            else:
                break
        return categories
    
    def _parse_price(self, price_str: str) -> float:
        """가격 문자열을 float으로 변환합니다."""
        if not price_str:
            return 0.0
        
        try:
            price_str = re.sub(r'[^\d.]', '', price_str)
            return float(price_str) if price_str else 0.0
        except ValueError:
            return 0.0
    
    def _create_product(self, item: dict) -> Product:
        """API 응답 아이템을 Product 객체로 변환합니다."""
        return Product(
            id=item.get("productId", ""),
            name=self._clean_html_tags(item.get("title", "")),
            price=self._parse_price(item.get("lprice", "0")),
            image_url=item.get("image", ""),
            url=item.get("link", ""),
            mall_name=self._clean_html_tags(item.get("mallName", "")),
            product_type=item.get("productType", ""),
            maker=self._clean_html_tags(item.get("maker", "")),
            categories=self._extract_categories(item)
        )
    
    async def fetch_product(self, query: str, display: int = 10, start: int = 1, sort: str = "sim") -> List[Product]:
        """
        네이버 쇼핑 API를 사용하여 제품을 검색합니다.
        
        Args:
            query: 검색 쿼리
            display: 표시할 결과 수 (1-100)
            start: 시작 인덱스
            sort: 정렬 방식 (sim, date, asc, dsc)
        
        Returns:
            Product 객체 리스트
        """
        try:
            display = max(1, min(100, display))
            start = max(1, start)
            
            encoded_query = urllib.parse.quote(query)
            url = f"/v1/search/shop.json?query={encoded_query}&display={display}&start={start}&sort={sort}"
            
            headers = {
                "X-Naver-Client-Id": self.client_id,
                "X-Naver-Client-Secret": self.client_secret
            }
            
            logger.debug(f"네이버 API 요청: {url}")
            logger.debug(f"Client ID: {self.client_id[:10]}..." if self.client_id else "Client ID: 없음")
            
            async with self.naver_client.get(url, headers=headers) as response:
                logger.debug(f"응답 상태: {response.status}")
                if response.status == 401:
                    logger.error("네이버 API 인증 실패: Client ID 또는 Secret이 올바르지 않습니다.")
                    return []
                
                response.raise_for_status()
                data = await response.json()
                
                items = data.get("items", [])
                products = []
                
                for item in items:
                    try:
                        product = self._create_product(item)
                        products.append(product)
                    except Exception as e:
                        logger.warning(f"제품 파싱 실패: {e}")
                        continue
                
                logger.info(f"{len(products)}개의 제품을 가져왔습니다.")
                return products
                
        except aiohttp.ClientError as e:
            logger.error(f"네이버 API 요청 실패: {e}")
            return []
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return []
    
    async def close(self):
        """세션을 닫습니다."""
        if self.naver_client and not self.naver_client.closed:
            await self.naver_client.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close() 