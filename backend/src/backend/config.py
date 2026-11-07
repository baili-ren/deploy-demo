from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    db_host: str = '127.0.0.1'
    db_port: int = 5432
    db_name: str = 'message_board'
    db_user: str = 'message_board'
    db_password: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()
