import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = os.getenv("MONGO_HOST")
    DB_PASS: str = os.getenv("MONGO_PASSWORD")
    DB_PORT: int = os.getenv("MONGO_PORT")
    DB_USER: str = os.getenv("MONGO_USER")
    DB_NAME: str = os.getenv("MONGO_DB")
    # DB_URL: str = os.getenv("MONGO_URL")
    DB_POOL_SIZE_MAX: int = os.getenv("MAX_CONNECTIONS_COUNT")
    DB_POOL_SIZE_MIN: int = os.getenv("MIN_CONNECTIONS_COUNT")

    @property
    def db_url(self) -> str:
        """
        Возвращает путь к базе данных
        """
        return f'mongodb://{self.DB_HOST}:{self.DB_PORT}'

@lru_cache()
def get_configuration():
    """
    Иницилизация конфигурации
    """
    cnf = Settings()
    return cnf


config = get_configuration()
