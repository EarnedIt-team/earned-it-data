from abc import ABC, abstractmethod
from typing import Optional

class ImageRepository(ABC):
    @abstractmethod
    def save_image(self, image_url: str, remove_background: bool = True) -> Optional[str]:
        """
        이미지를 저장합니다.

        :param image_url: 저장할 이미지의 URL
        :param remove_background: 배경 제거 여부
        :return: 저장된 S3 이미지 URL (없으면 None)
        """
        ...

    @abstractmethod
    def get_image(self, image_id: str) -> str:
        """
        이미지 ID를 사용하여 이미지를 가져옵니다.

        :param image_id: 검색할 이미지의 ID
        :return: 이미지의 URL
        """
        ...