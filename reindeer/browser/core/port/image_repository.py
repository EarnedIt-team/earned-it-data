from abc import ABC, abstractmethod


class ImageRepository(ABC):
    @abstractmethod
    def save_image(self, image_url: str) -> bool:
        """
        이미지를 저장합니다.

        :param image_url: 저장할 이미지의 URL
        :return: 저장 성공 여부
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