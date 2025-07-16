from fastapi import APIRouter, HTTPException, Query
from app.dto.product_dto import SearchRequest, SearchResponse, ProductResponse
from browser.task.search import search_product

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
    responses={
        404: {"description": "리소스를 찾을 수 없습니다"},
        500: {"description": "서버 내부 오류가 발생했습니다"},
        503: {"description": "데이터베이스 서비스를 사용할 수 없습니다"},
    },
)


@router.get("/search", 
           response_model=SearchResponse,
           summary="제품 검색 (GET)",
           description="쿼리 파라미터를 사용하여 제품을 검색합니다.",
           response_description="검색된 제품 목록과 관련 정보")
async def search_products_get(
    query: str = Query(..., 
                      description="검색어", 
                      example="아이폰 14",
                      min_length=1,
                      max_length=100),
    use_cache: bool = Query(True, 
                            description="캐시 사용 여부", 
                            example=True),
    remove_background: bool = Query(True, 
                                    description="배경 제거 여부", 
                                    example=True),

):
    """
    ## GET 방식으로 제품을 검색합니다.
    
    ### 파라미터 설명
    - **query**: 검색할 제품명 또는 키워드
    - **use_cache**: 캐시 사용 여부
    - **remove_background**: 배경 제거 여부
    
    ### 응답 정보
    - 검색된 제품 목록
    - 각 제품의 상세 정보 (이름, 가격, 이미지, URL 등)
    - 검색 메타데이터 (총 개수, 현재 페이지 등)
    """
    request = SearchRequest(
        query=query,
        use_cache=use_cache,
        remove_background=remove_background
    )
    
    try:
        # 제품 검색 실행
        products = await search_product(
            query=request.query,
            use_cache=request.use_cache,
            remove_background=request.remove_background
        )
        
        # DTO 변환
        product_responses = [
            ProductResponse.model_validate(product)
            for product in products
        ]
        
        return SearchResponse(
            products=product_responses,
            total_count=len(product_responses),
            query=request.query,
            use_cache=request.use_cache,
            remove_background=request.remove_background
        )
        
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "pool" in error_msg.lower():
            raise HTTPException(
                status_code=503, 
                detail="데이터베이스 연결을 사용할 수 없습니다. PostgreSQL 서버를 확인하세요."
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"검색 중 오류가 발생했습니다: {str(e)}"
            )


