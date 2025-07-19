from typing import List
from abc import ABC, abstractmethod
from browser.core.entity.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def save_product(self, product: Product) -> None:
        """
        제품 정보를 저장합니다.

        :param product: 저장할 제품 객체
        :return: 없음
        """
        ...

    @abstractmethod
    def get_product(self, product_id: str) -> Product:
        """
        제품 ID를 사용하여 제품 정보를 가져옵니다.

        :param product_id: 검색할 제품의 ID
        :return: 제품 객체
        """
        ...

    @abstractmethod
    def search_products(self, query: str, limit: int = 50, offset: int = 0) -> List[Product]:
        """
        제품명으로 제품을 검색합니다.
        """
        ...