from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = "sqlite:///:memory:"
    db_echo: bool = True

    base_url: str = "https://test.deribit.com/api/v2/"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
