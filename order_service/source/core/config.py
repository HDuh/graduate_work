import os
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from .logger import LOGGING

__all__ = (
    'settings',
)

load_dotenv()
logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = '...'
    logging = LOGGING

    class Config:
        env_prefix = 'glob_'
        env_file = os.path.join(BASE_DIR, '.env')
        case_sensitive = False


class PostgresConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    database_uri: str = Field(..., env='SQLALCHEMY_DATABASE_URI')
    db_echo_log: bool = Field(..., env='SQLALCHEMY_DB_ECHO_LOG')

    class Config:
        env_prefix = 'sqlalchemy_'
        # env_file = os.path.join(BASE_DIR, '.env')
        case_sensitive = False


class Settings(BaseSettings):
    app = AppConfig()
    postgres_config = PostgresConfig()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
