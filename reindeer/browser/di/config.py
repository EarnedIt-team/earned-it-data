from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    log_level: str | None = None
    environment: str | None = None
    
    # PostgreSQL settings
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    
    # S3 settings
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "product-images"
    s3_timeout: int = 20
    
    # Naver API settings
    naver_client_id: str
    naver_client_secret: str
    naver_base_url: str
    naver_timeout: int = 10
