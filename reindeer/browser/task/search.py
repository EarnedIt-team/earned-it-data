import asyncio
from dependency_injector.wiring import Provide, inject
from browser.di.base import BaseContainer
from browser.di.config import Settings
from browser.core.usecase.search_product import SearchProduct

# 전역 컨테이너 인스턴스
container = None

async def init():
    global container
    container = BaseContainer()
    container.wire(modules=[__name__])
    config = Settings()
    container.config.from_pydantic(config)
    await container.init_resources()
    print("container initialized")


async def cleanup():
    """컨테이너와 리소스를 정리합니다."""
    global container
    if container:
        try:
            await container.shutdown_resources()
            print("container resources cleaned up")
        except Exception as e:
            print(f"container cleanup error: {e}")
        finally:
            container = None


@inject
async def search_product(
    query: str, 
    use_cache: bool = True,
    remove_background: bool = True,
    search_usecase: SearchProduct = Provide[BaseContainer.search_product]
):
    """
    제품 검색 함수
    """
    try:        
        # 검색 실행
        products = await search_usecase.search_product(
            query=query,
            use_cache=use_cache,
            remove_background=remove_background
        )
        
        return products
    except Exception as e:
        print(f"❌ 제품 검색 중 오류: {e}")
        return []