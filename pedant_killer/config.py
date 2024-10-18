import os

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Config(BaseSettings):
    TG_API_DIGIT_SPACE_BOT: SecretStr = os.getenv('TG_API_DIGIT_SPACE_BOT')

    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_NAME: str = os.getenv('DB_NAME')

    @property
    def database_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


config = Config()
