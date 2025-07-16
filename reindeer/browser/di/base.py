from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from browser.di.config import Settings
from browser.core.infra.postgresql_client import create_postgresql_pool
from browser.core.infra.s3_client import get_s3_client, get_s3_config, create_http_session
from browser.core.infra.naver_client import create_naver_client
from browser.adapter.repository.postgresql_repository import PostgreSQLRepository
from browser.adapter.repository.s3_repository import S3Repository
from browser.adapter.product_fetcher.naver_fetcher import NaverFetcher
from browser.core.usecase.search_product import SearchProduct
import aiohttp


class BaseContainer(DeclarativeContainer):
    config: Settings = providers.Configuration()
    
    # Database clients
    postgresql_pool = providers.Resource(
        create_postgresql_pool,
        db_host=config.db_host,
        db_port=config.db_port,
        db_user=config.db_user,
        db_password=config.db_password,
        db_name=config.db_name,
    )
    
    # S3 clients
    s3_client = providers.Singleton(
        get_s3_client,
    )
    
    s3_config = providers.Singleton(
        get_s3_config,
    )
    
    # HTTP session resources (generator 함수를 사용한 Resource)
    http_session = providers.Resource(
        create_http_session,
        timeout=config.s3_timeout,
    )
    
    # Naver client resource (generator 함수를 사용한 Resource)
    naver_client = providers.Resource(
        create_naver_client,
        base_url=config.naver_base_url,
        timeout=config.naver_timeout,
    )
    
    # Repositories
    postgresql_repository = providers.Singleton(
        PostgreSQLRepository,
        connection_pool=postgresql_pool,
    )
    
    s3_repository = providers.Singleton(
        S3Repository,
        s3_client=s3_client,
        bucket_name=config.s3_bucket_name,
        http_session=http_session,
    )
    
    # Product fetchers
    naver_fetcher = providers.Singleton(
        NaverFetcher,
        naver_client=naver_client,
        client_id=config.naver_client_id,
        client_secret=config.naver_client_secret,
    )
    
    # Usecases
    search_product = providers.Singleton(
        SearchProduct,
        product_fetcher=naver_fetcher,
        product_repository=postgresql_repository,
        image_repository=s3_repository,
    )

