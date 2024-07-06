from abc import ABC, abstractmethod
from psycopg2 import extensions

from src.config import settings


class DBManager(ABC):
    """
    Класс менеджер для работы с БД наследующийся от абстрактного класса
    """
    def __init__(self, db_name: str = settings.DB_NAME):
        """
        Метод инициализирующий параметры для БД
        """
        self.db_name = db_name
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT
        self.connection: extensions.connection | None = None

    @abstractmethod
    def connect(self) -> None:
        """
        Абстрактный метод для подключения к БД
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Абстрактный метод для отключения от БД
        """
        pass

    def commit(self) -> None:
        """
        Метод для коммита в БД
        """
        self.connection.commit()
