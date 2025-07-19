import asyncpg
import os
import logging
from typing import Optional, List
from browser.core.port.product_repository import ProductRepository
from browser.core.entity.product import Product
import json
import asyncio

logger = logging.getLogger(__name__)


class PostgreSQLRepository(ProductRepository):
    def __init__(self, connection_pool: asyncpg.Pool):
        self.connection_pool = connection_pool
        self._initialized = False
        self._init_lock = asyncio.Lock()
    
    async def _ensure_initialized(self):
        """데이터베이스 초기화를 보장합니다."""
        if not self._initialized:
            async with self._init_lock:
                if not self._initialized:
                    await self.create_table()
                    self._initialized = True
    
    async def save_product(self, product: Product) -> None:
        """제품 정보를 데이터베이스에 저장합니다."""
        await self.save_products([product])
    
    async def save_products(self, products: List[Product]) -> None:
        """여러 제품을 배치로 저장합니다."""
        if not products:
            return
        
        await self._ensure_initialized()
        
        async with self.connection_pool.acquire() as conn:
            query = """
            INSERT INTO products (
                id, name, price, image_url, url, mall_name, 
                product_type, maker, categories, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                price = EXCLUDED.price,
                image_url = EXCLUDED.image_url,
                url = EXCLUDED.url,
                mall_name = EXCLUDED.mall_name,
                product_type = EXCLUDED.product_type,
                maker = EXCLUDED.maker,
                categories = EXCLUDED.categories,
                updated_at = NOW()
            """
            
            batch_data = []
            for product in products:
                batch_data.append((
                    product.id,
                    product.name,
                    product.price,
                    product.image_url,
                    product.url,
                    product.mall_name,
                    product.product_type,
                    product.maker,
                    json.dumps(product.categories, ensure_ascii=False)
                ))
            
            await conn.executemany(query, batch_data)
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """제품 ID로 제품 정보를 조회합니다."""
        await self._ensure_initialized()
        
        async with self.connection_pool.acquire() as conn:
            query = """
            SELECT id, name, price, image_url, url, mall_name, 
                   product_type, maker, categories
            FROM products 
            WHERE id = $1
            """
            
            result = await conn.fetchrow(query, product_id)
            
            if result:
                return self._create_product_from_db(dict(result))
            
            return None
    
    async def get_products(self, product_ids: List[str]) -> List[Product]:
        """여러 제품 ID로 제품 정보를 배치 조회합니다."""
        if not product_ids:
            return []
        
        await self._ensure_initialized()
        
        async with self.connection_pool.acquire() as conn:
            query = """
            SELECT id, name, price, image_url, url, mall_name, 
                   product_type, maker, categories
            FROM products 
            WHERE id = ANY($1)
            """
            
            results = await conn.fetch(query, product_ids)
            
            products = []
            for result in results:
                product = self._create_product_from_db(dict(result))
                if product:
                    products.append(product)
            
            return products
    
    async def search_products(self, query: str, limit: int = 50, offset: int = 0) -> List[Product]:
        """제품명으로 제품을 검색합니다."""
        await self._ensure_initialized()
        
        async with self.connection_pool.acquire() as conn:
            search_query = """
            SELECT id, name, price, image_url, url, mall_name, 
                   product_type, maker, categories
            FROM products 
            WHERE name ILIKE $1
            ORDER BY updated_at DESC
            LIMIT $2 OFFSET $3
            """
            
            search_term = f"%{query}%"
            results = await conn.fetch(search_query, search_term, limit, offset)
            
            products = []
            for result in results:
                product = self._create_product_from_db(dict(result))
                if product:
                    products.append(product)
            
            return products
    
    def _create_product_from_db(self, result: dict) -> Optional[Product]:
        """데이터베이스 결과를 Product 객체로 변환합니다."""
        try:
            categories = json.loads(result['categories']) if result['categories'] else []
            
            return Product(
                id=result['id'],
                name=result['name'],
                price=result['price'],
                image_url=result['image_url'],
                url=result['url'],
                mall_name=result['mall_name'],
                product_type=result['product_type'],
                maker=result['maker'],
                categories=categories
            )
        except Exception as e:
            logger.error(f"제품 생성 중 오류: {e}")
            return None
    
    async def create_table(self):
        """제품 테이블을 생성합니다."""
        logger.info("PostgreSQL 테이블 초기화 중...")
        
        async with self.connection_pool.acquire() as conn:
            create_query = """
            CREATE TABLE IF NOT EXISTS products (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(1000) NOT NULL,
                price DECIMAL(10, 2) DEFAULT 0.00,
                image_url TEXT,
                url TEXT,
                mall_name VARCHAR(255),
                product_type VARCHAR(255),
                maker VARCHAR(255),
                categories JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
            CREATE INDEX IF NOT EXISTS idx_products_mall_name ON products(mall_name);
            CREATE INDEX IF NOT EXISTS idx_products_updated_at ON products(updated_at);
            """
            
            await conn.execute(create_query)
            logger.info("PostgreSQL 테이블 초기화 완료")
    
    async def close(self):
        """연결 풀을 닫습니다."""
        if self.connection_pool:
            await self.connection_pool.close() 