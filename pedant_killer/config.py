from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, computed_field


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    TG_API_DIGIT_SPACE_BOT: SecretStr

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str

    API_YANDEX_MAP: str

    @computed_field
    @property
    def database_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @computed_field
    @property
    def test_database_url_asyncpg(self) -> str:
        return (f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:'
                f'{self.DB_PORT_TEST}/{self.DB_NAME_TEST}')


config = Config()
