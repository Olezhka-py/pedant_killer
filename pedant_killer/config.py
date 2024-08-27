import os

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Config(BaseSettings):
    TG_API_DIGIT_SPACE_BOT: SecretStr = os.getenv('TG_API_DIGIT_SPACE_BOT')


config = Config()
