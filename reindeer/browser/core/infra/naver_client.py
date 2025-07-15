from functools import lru_cache
import aiohttp


@lru_cache
async def create_naver_client(base_url: str, timeout: int = 10) -> aiohttp.ClientSession:
    """네이버 클라이언트 세션을 생성합니다."""
    return aiohttp.ClientSession(base_url=base_url, timeout=aiohttp.ClientTimeout(total=timeout))