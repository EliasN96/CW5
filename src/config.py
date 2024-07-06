import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()


class Settings:
    """
    Класс для настройки БД
    """
    DB_NAME = 'cw5'
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    EMPLOYEE_IDS_CONFIG = BASE_DIR.joinpath('ten_employers.json')
    MIGRATIONS_DIR = BASE_DIR.joinpath('src', 'migrations')

    def get_employer_ids(self) -> list[int]:
        """
        Метод для получения идентификаторов работодателей
        """
        with self.EMPLOYEE_IDS_CONFIG.open() as f:
            data = json.load(f)

            return data['employers']['hh']


settings = Settings()
