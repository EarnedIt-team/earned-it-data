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
    
    async def search_product(self, query: str, use_cache: bool = True, remove_background: bool = True) -> List[Product]:
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
            products = await self.product_fetcher.fetch_product(query)
            
            if not products:
                return []
            
            # 3. 배치 처리로 이미지 저장 및 제품 정보 저장
            await self._save_products_batch(products, remove_background=remove_background)
            
            # 4. 캐시 저장 (첫 번째 제품을 캐시로 저장)
            if products and use_cache:
                await self.product_repository.save_product(products[0])
            
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
            # 이미지 저장 작업들을 병렬로 실행
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
            
            # 제품 정보 저장 작업들을 병렬로 실행
            product_tasks = [
                self.product_repository.save_product(product)
                for product in products
            ]
            
            # 모든 작업을 병렬로 실행
            await asyncio.gather(
                *image_tasks,
                *product_tasks,
                return_exceptions=True
            )
            
        except Exception as e:
            print(f"배치 저장 중 오류 발생: {e}")
    
