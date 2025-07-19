import asyncpg
from functools import lru_cache
import os


@lru_cache
def get_postgresql_config():
    """PostgreSQL 연결 설정을 반환합니다."""
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'product_db'),
        'min_size': 5,
        'max_size': 20,
    }
    
    # 디버깅을 위한 연결 정보 출력 (비밀번호는 마스킹)
    print(f"🔍 PostgreSQL 연결 설정:")
    print(f"   호스트: {config['host']}")
    print(f"   포트: {config['port']}")
    print(f"   사용자: {config['user']}")
    print(f"   비밀번호: {'*' * len(config['password']) if config['password'] else '(없음)'}")
    print(f"   데이터베이스: {config['database']}")
    
    return config


async def create_postgresql_pool(db_host: str, db_port: int, db_user: str, db_password: str, db_name: str):
    """PostgreSQL 연결 풀을 생성합니다."""
    config = {
        'host': db_host,
        'port': db_port,
        'user': db_user,
        'password': db_password,
        'database': db_name,
    }
    
    try:
        print(f"🔌 PostgreSQL 연결 시도 중: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
        pool = await asyncpg.create_pool(**config)
        print(f"✅ PostgreSQL 연결 성공")
        return pool
    except Exception as e:
        print(f"❌ PostgreSQL 연결 실패: {e}")
        print(f"🔍 연결 시도한 설정: {config['host']}:{config['port']}")
        raise e