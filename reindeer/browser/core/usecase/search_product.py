from browser.core.port.product_fetcher import ProductFetcher
from browser.core.port.product_repository import ProductRepository
from browser.core.port.image_repository import ImageRepository
from browser.core.entity.product import Product
from typing import List, Optional
import asyncio
import hashlib
from pydantic import BaseModel

class SearchProductRequest(BaseModel):
    query: str
    use_cache: bool = True
    remove_background: bool = True

class SearchProduct:
    def __init__(self, product_fetcher: ProductFetcher, product_repository: ProductRepository, image_repository: ImageRepository):
        self.product_fetcher = product_fetcher
        self.product_repository = product_repository
        self.image_repository = image_repository
    
    async def search_product(self, query: str, use_cache: bool = True, remove_background: bool = True, display: int = 10) -> List[Product]:
        """
        제품을 검색합니다.
        
        :param query: 검색 쿼리
        :param use_cache: 캐시 사용 여부
        :param remove_background: 배경 제거 여부
        :return: 제품 리스트
        """
        
        # 1. 캐시 확인 (선택적)
        if use_cache:
            cached_product = await self.product_repository.search_products(query)
            if cached_product:
                return cached_product
        
        # 2. 외부 API에서 제품 정보 가져오기
        try:
            products = await self.product_fetcher.fetch_product(query, display=display)
            
            if not products:
                return []
            
            # 3. 배치 처리로 이미지 저장 및 제품 정보 저장
            await self._save_products_batch(products, remove_background=remove_background)
            
            return products
            
        except Exception as e:
            print(f"제품 검색 중 오류 발생: {e}")
            return []
    
    async def _save_products_batch(self, products: List[Product], remove_background: bool = True) -> None:
        """
        제품들을 배치로 저장합니다.
        
        :param products: 저장할 제품 리스트
        :param remove_background: 배경 제거 여부
        """
        try:
            # 이미지 저장 작업들을 병렬로 실행하고 S3 URL을 받아옴
            image_tasks = []
            for product in products:
                if product.image_url:
                    # S3Repository의 save_image 메서드를 사용 (배경 제거 옵션 포함)
                    if hasattr(self.image_repository, 'save_image'):
                        image_tasks.append(
                            self.image_repository.save_image(
                                product.image_url, 
                                remove_background=remove_background
                            )
                        )
                    else:
                        # 기본 save_image 메서드 사용
                        image_tasks.append(
                            self.image_repository.save_image(product.image_url)
                        )
                else:
                    # 이미지가 없는 경우 None을 반환하는 더미 코루틴
                    async def dummy_task():
                        return None
                    image_tasks.append(dummy_task())
            
            # 이미지 저장 결과를 받아서 Product의 image_url 업데이트
            if image_tasks:
                image_results = await asyncio.gather(*image_tasks, return_exceptions=True)
                
                # Product 객체의 image_url을 S3 URL로 업데이트
                for i, (product, s3_url) in enumerate(zip(products, image_results)):
                    if isinstance(s3_url, str) and s3_url:  # 성공적으로 S3 URL을 받은 경우
                        # Product는 pydantic 모델이므로 새로운 인스턴스 생성
                        updated_product = Product(
                            id=product.id,
                            name=product.name,
                            price=product.price,
                            image_url=s3_url,  # S3 URL로 교체
                            url=product.url,
                            mall_name=product.mall_name,
                            product_type=product.product_type,
                            maker=product.maker,
                            categories=product.categories
                        )
                        products[i] = updated_product  # 리스트의 해당 인덱스를 업데이트
                    elif isinstance(s3_url, Exception):
                        print(f"이미지 저장 중 오류: {s3_url}")
            
            # 제품 정보 저장 작업들을 병렬로 실행 (업데이트된 S3 URL 포함)
            product_tasks = [
                self.product_repository.save_product(product)
                for product in products
            ]
            
            # 제품 정보 저장 실행
            await asyncio.gather(*product_tasks, return_exceptions=True)
            
        except Exception as e:
            print(f"배치 저장 중 오류 발생: {e}")
    
