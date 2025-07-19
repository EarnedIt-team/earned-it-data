import boto3
import aiohttp
from functools import lru_cache
import os
from contextlib import asynccontextmanager


@lru_cache
def get_s3_client():
    """S3 클라이언트를 생성합니다."""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )


@lru_cache
def get_s3_config():
    """S3 설정을 반환합니다."""
    return {
        'bucket_name': os.getenv('S3_BUCKET_NAME', 'product-images'),
        'region': os.getenv('AWS_REGION', 'us-east-1')
    }


@asynccontextmanager
async def create_http_session_context(timeout: int = 20):
    """HTTP 세션을 생성하고 적절히 정리하는 async context manager입니다."""
    timeout_config = aiohttp.ClientTimeout(total=timeout)
    session = aiohttp.ClientSession(timeout=timeout_config)
    print(f"🔧 HTTP 세션 생성됨: {id(session)}")
    try:
        yield session
    finally:
        await session.close()
        print(f"🔧 HTTP 세션 닫힘: {id(session)}")


async def create_http_session(timeout: int = 20):
    """HTTP 세션을 생성하고 적절히 정리하는 generator 함수입니다."""
    timeout_config = aiohttp.ClientTimeout(total=timeout)
    session = aiohttp.ClientSession(timeout=timeout_config)
    print(f"🔧 HTTP 세션 생성됨: {id(session)}")
    try:
        yield session
    finally:
        await session.close()
        print(f"🔧 HTTP 세션 닫힘: {id(session)}")
