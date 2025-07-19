from abc import ABC, abstractmethod
from typing import List
from browser.core.entity.product import Product


class ProductFetcher(ABC):
    @abstractmethod
    async def fetch_product(self, query: str, display: int = 10, start: int = 1, sort: str = "sim") -> List[Product]:
        """
        검색어를 사용하여 제품 정보를 가져옵니다.

        :param query: 검색할 제품의 검색어
        :param display: 표시할 결과 수 (1-100)
        :param start: 시작 인덱스
        :param sort: 정렬 방식 (sim, date, asc, dsc)
        :return: 제품 객체 리스트
        """
        ...