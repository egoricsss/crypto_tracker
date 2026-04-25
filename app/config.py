import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://crypto_user:crypto_password@db:5432/crypto_tracker")
    db_echo: bool = True

    base_url: str = "https://test.deribit.com/api/v2/"
    
    # Celery settings
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
