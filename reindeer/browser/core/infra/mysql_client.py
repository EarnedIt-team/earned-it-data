import aiomysql
from functools import lru_cache
import os


@lru_cache
def get_mysql_client():
    """MySQL 연결 설정을 반환합니다."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'db': os.getenv('DB_NAME', 'product_db'),
        'charset': 'utf8mb4',
        'autocommit': True,
        'maxsize': 20,
        'minsize': 5,
        'echo': False
    }


async def create_mysql_pool():
    """MySQL 연결 풀을 생성합니다."""
    config = get_mysql_client()
    return await aiomysql.create_pool(**config)
