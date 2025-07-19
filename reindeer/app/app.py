from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.router import product_router
from browser.task.search import init, cleanup

# FastAPI 앱 생성
app = FastAPI(
    title="🦌 Reindeer Product Search API",
    description="""
    제품 검색 engine server
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Reindeer API Support",
        "email": "support@reindeer.dev",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.reindeer.dev",
            "description": "Production server"
        }
    ]
)

# 애플리케이션 시작 시 리소스 초기화
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 리소스를 초기화합니다."""
    print("🚀 애플리케이션 시작 중...")
    await init()
    print("✅ 애플리케이션 시작 완료")


# 애플리케이션 종료 시 리소스 정리
@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 리소스를 정리합니다."""
    print("🛑 애플리케이션 종료 중...")
    await cleanup()
    print("✅ 애플리케이션 종료 완료")


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 실제 운영에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(product_router)

# 간단한 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """간단한 헬스체크 - 200 상태 반환"""
    return {"status": "OK"}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "🦌 Reindeer Product Search API is running"}


def custom_openapi():
    """커스텀 OpenAPI 스키마 생성"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="🦌 Reindeer Product Search API",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # 태그 정보 추가
    openapi_schema["tags"] = [
        {
            "name": "products",
            "description": "제품 검색 및 관리 API",
        },
        {
            "name": "health",
            "description": "서비스 상태 확인 API",
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# 메인 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
