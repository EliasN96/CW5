from abc import ABC, abstractmethod
import requests


class APIClient(ABC):
    """
    Абстрактный класс для работы с API
    """

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        Абстрактный метод получения ссылки на hh.ru
        """
        pass

    def _get(self, url: str, params: dict = {}) -> dict:
        """
        Метод получения информации возвращающий словарь
        """
        full_url = self.base_url + url

        response = requests.get(full_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
