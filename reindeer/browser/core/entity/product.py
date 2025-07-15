from pydantic import BaseModel


class Product(BaseModel):
    """
    제품 정보를 나타내는 클래스입니다.
    
    속성:
        id (str): 제품의 고유 식별자
        name (str): 제품의 이름
        price (float): 제품의 가격
        image_url (str): 제품 이미지의 URL
        url (str): 제품의 상세 페이지 URL
        mall_name (str): 제품이 판매되는 쇼핑몰의 이름
        product_type (str): 제품의 유형
        maker (str): 제품의 제조사
        categories (list[str]): 제품이 속한 카테고리 목록
    """
    id: str
    name: str
    price: float
    image_url: str
    url: str
    mall_name: str
    product_type: str
    maker: str
    categories: list[str]