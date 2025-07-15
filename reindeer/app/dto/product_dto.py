from pydantic import BaseModel, Field
from typing import List, Optional


class ProductResponse(BaseModel):
    """제품 응답 DTO"""
    id: str = Field(..., description="제품 고유 ID", example="PRD123456")
    name: str = Field(..., description="제품명", example="아이폰 14 프로 128GB")
    price: float = Field(..., description="가격 (원)", example=1299000.0)
    image_url: str = Field(..., description="제품 이미지 URL", example="https://example.com/image.jpg")
    url: str = Field(..., description="제품 상세 페이지 URL", example="https://shopping.naver.com/product/123")
    mall_name: str = Field(..., description="쇼핑몰명", example="네이버쇼핑")
    product_type: str = Field(..., description="제품 타입", example="1")
    maker: str = Field(..., description="제조사", example="Apple")
    categories: List[str] = Field(
        default=[], 
        description="카테고리 목록", 
        example=["디지털/가전", "휴대폰", "스마트폰"]
    )
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "PRD123456",
                "name": "아이폰 14 프로 128GB 딥퍼플",
                "price": 1299000.0,
                "image_url": "https://example.com/iphone14.jpg",
                "url": "https://shopping.naver.com/product/123456",
                "mall_name": "애플스토어",
                "product_type": "1",
                "maker": "Apple",
                "categories": ["디지털/가전", "휴대폰", "스마트폰", "아이폰"]
            }
        }


class SearchRequest(BaseModel):
    """검색 요청 DTO"""
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="검색어",
        example="아이폰 14"
    )
    use_cache: bool = Field(
        default=True, 
        description="캐시 사용 여부", 
        example=True
    )
    remove_background: bool = Field(
        default=True, 
        description="배경 제거 여부", 
        example=True
    )
    
    class Config:
        schema_extra = {
            "example": {
                "query": "아이폰 14",
                "use_cache": True,
                "remove_background": True
            }
        }


class SearchResponse(BaseModel):
    """검색 응답 DTO"""
    products: List[ProductResponse] = Field(
        ..., 
        description="검색된 제품 목록"
    )
    total_count: int = Field(
        ..., 
        description="검색된 제품 총 개수",
        example=10
    )
    query: str = Field(
        ..., 
        description="검색어",
        example="아이폰 14"
    )
    use_cache: bool = Field(
        default=True, 
        description="캐시 사용 여부", 
        example=True
    )
    remove_background: bool = Field(
        default=True, 
        description="배경 제거 여부", 
        example=True
    )
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "products": [
                    {
                        "id": "PRD123456",
                        "name": "아이폰 14 프로 128GB 딥퍼플",
                        "price": 1299000.0,
                        "image_url": "https://example.com/iphone14.jpg",
                        "url": "https://shopping.naver.com/product/123456",
                        "mall_name": "애플스토어",
                        "product_type": "1",
                        "maker": "Apple",
                        "categories": ["디지털/가전", "휴대폰", "스마트폰", "아이폰"]
                    }
                ],
                "total_count": 1,
                "query": "아이폰 14",
                "use_cache": True,
                "remove_background": True
            }
        } 