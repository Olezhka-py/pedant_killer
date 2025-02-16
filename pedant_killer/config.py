import os

from pydantic_settings import BaseSettings
from pydantic import SecretStr, computed_field


class Config(BaseSettings):
    TG_API_DIGIT_SPACE_BOT: SecretStr

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @computed_field
    @property
    def database_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


config = Config()
