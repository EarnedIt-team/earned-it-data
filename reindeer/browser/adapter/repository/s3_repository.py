import boto3
import aiohttp
import os
import logging
from typing import Optional
from browser.core.port.image_repository import ImageRepository
import hashlib
import asyncio
from botocore.exceptions import ClientError
from PIL import Image
from rembg import remove
import io

logger = logging.getLogger(__name__)


class S3Repository(ImageRepository):
    def __init__(self, s3_client, bucket_name: str, http_session: aiohttp.ClientSession):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.session = http_session
    
    def _generate_image_id(self, image_url: str) -> str:
        """이미지 URL을 기반으로 고유한 이미지 ID를 생성합니다."""
        return hashlib.md5(image_url.encode()).hexdigest()
    
    def _get_s3_key(self, image_id: str, with_background: bool = True) -> str:
        """S3 키를 생성합니다."""
        if with_background:
            return f"images/original/{image_id}.jpg"
        else:
            return f"images/no-bg/{image_id}.png"
    
    async def _remove_background(self, image_data: bytes) -> Optional[bytes]:
        """
        이미지에서 배경을 제거합니다.
        
        Args:
            image_data: 원본 이미지 바이트 데이터
        
        Returns:
            배경이 제거된 PNG 이미지 바이트 데이터
        """
        try:
            input_image = Image.open(io.BytesIO(image_data))
            
            output_image = await asyncio.get_event_loop().run_in_executor(
                None, remove, input_image
            )
            
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format='PNG')
            output_buffer.seek(0)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"배경 제거 중 오류 발생: {e}")
            return None
    
    async def save_image(self, image_url: str, remove_background: bool = True) -> bool:
        """
        이미지를 다운로드하고 S3에 저장합니다.
        
        Args:
            image_url: 이미지 URL
            remove_background: 배경 제거 여부
        
        Returns:
            저장 성공 여부
        """
        try:
            image_id = self._generate_image_id(image_url)
            
            original_key = self._get_s3_key(image_id, with_background=True)
            
            no_bg_key = self._get_s3_key(image_id, with_background=False) if remove_background else None
            
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=original_key)
                if remove_background and no_bg_key:
                    try:
                        self.s3_client.head_object(Bucket=self.bucket_name, Key=no_bg_key)
                        return True
                    except ClientError as e:
                        if e.response['Error']['Code'] != '404':
                            raise
                else:
                    return True
            except ClientError as e:
                if e.response['Error']['Code'] != '404':
                    raise
            
            async with self.session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.s3_client.put_object(
                            Bucket=self.bucket_name,
                            Key=original_key,
                            Body=image_data,
                            ContentType='image/jpeg'
                        )
                    )
                    
                    if remove_background and no_bg_key:
                        logger.info(f"배경 제거 중: {image_url}")
                        no_bg_data = await self._remove_background(image_data)
                        
                        if no_bg_data:
                            await asyncio.get_event_loop().run_in_executor(
                                None,
                                lambda: self.s3_client.put_object(
                                    Bucket=self.bucket_name,
                                    Key=no_bg_key,
                                    Body=no_bg_data,
                                    ContentType='image/png'
                                )
                            )
                            logger.info(f"배경 제거 완료: {image_url}")
                        else:
                            logger.warning(f"배경 제거 실패: {image_url}")
                    
                    return True
                else:
                    logger.error(f"이미지 다운로드 실패: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"이미지 저장 중 오류 발생: {e}")
            return False
    
    async def save_image_with_background_removal(self, image_url: str) -> bool:
        """
        이미지를 다운로드하고 배경을 제거하여 S3에 저장합니다.
        
        Args:
            image_url: 이미지 URL
        
        Returns:
            저장 성공 여부
        """
        return await self.save_image(image_url, remove_background=True)
    
    async def get_image(self, image_id: str, with_background: bool = True) -> Optional[str]:
        """
        이미지 ID로 S3에서 이미지 URL을 조회합니다.
        
        Args:
            image_id: 이미지 ID
            with_background: 배경 포함 여부
        
        Returns:
            이미지 URL
        """
        try:
            s3_key = self._get_s3_key(image_id, with_background=with_background)
            
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    return None
                raise
            
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=3600
            )
            
            return url
            
        except Exception as e:
            logger.error(f"이미지 조회 중 오류 발생: {e}")
            return None
    
    async def get_image_by_url(self, original_url: str, with_background: bool = True) -> Optional[str]:
        """
        원본 URL로 저장된 이미지의 S3 URL을 조회합니다.
        
        Args:
            original_url: 원본 이미지 URL
            with_background: 배경 포함 여부
        
        Returns:
            S3 이미지 URL
        """
        image_id = self._generate_image_id(original_url)
        return await self.get_image(image_id, with_background=with_background)
    
    async def get_no_background_image(self, image_id: str) -> Optional[str]:
        """
        배경이 제거된 이미지를 조회합니다.
        
        Args:
            image_id: 이미지 ID
        
        Returns:
            배경이 제거된 이미지 URL
        """
        return await self.get_image(image_id, with_background=False)
    
    async def get_no_background_image_by_url(self, original_url: str) -> Optional[str]:
        """
        원본 URL로 배경이 제거된 이미지를 조회합니다.
        
        Args:
            original_url: 원본 이미지 URL
        
        Returns:
            배경이 제거된 이미지 URL
        """
        return await self.get_image_by_url(original_url, with_background=False)
    
    async def close(self):
        """세션을 닫습니다."""
        if self.session and not self.session.closed:
            await self.session.close()
