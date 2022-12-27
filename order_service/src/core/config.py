import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings

from .logger import LOGGING

__all__ = (
    'settings',
    'OrderStatus',
    'SubscriptionStatus',
    'ProductTypes',
)

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str
    test_user_id: str
    logging = LOGGING
    log_level: str

    class Config:
        env_prefix = 'glob_'
        case_sensitive = False


class PostgresConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    database_uri: str
    db_echo_log: bool

    class Config:
        env_prefix = 'sqlalchemy_'
        case_sensitive = False


class StripeConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    publish_key: str
    secret_key: str

    class Config:
        env_prefix = 'stripe_'
        case_sensitive = False


class BillingConfig(BaseSettings):
    """
    Конфигурация сервиса billing
    """
    checkout_session_url: str

    class Config:
        env_prefix = 'billing_'
        case_sensitive = False


class Settings(BaseSettings):
    app = AppConfig()
    db_config = PostgresConfig()
    stripe_config = StripeConfig()
    billing_config = BillingConfig()


class OrderStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    ERROR = "error"
    CANCELED = "canceled"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"


class ProductTypes(Enum):
    SUBSCRIPTION = 'subscription'


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
