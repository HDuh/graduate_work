import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

__all__ = (
    'settings',
    'PaymentState',
    'SubscriptionStatus',
    'WebhookEvents',
)

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str
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
    db_echo_log: bool = True

    class Config:
        env_prefix = 'billing_sqlalchemy_'
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


class Settings(BaseSettings):
    app = AppConfig()
    db_config = PostgresConfig()
    stripe_config = StripeConfig()


class PaymentState(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    ERROR = "error"
    CANCELED = "canceled"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"


class WebhookEvents(str, Enum):
    PAYMENT_SUCCESS = 'checkout.session.completed'
    PAYMENT_REFUND = 'customer.subscription.deleted'


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
