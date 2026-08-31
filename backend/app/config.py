from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_name: str = "Wealth Conversational Finance Assistant"
    secret_key: str = "development-only-change-me"
    access_token_expire_minutes: int = Field(default=30, ge=5, le=1440)
    frontend_url: str = "http://localhost:3000"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "wealth_assistant"
    database_backend: Literal["mongodb", "memory"] = "mongodb"

    ai_provider: Literal["mock", "openai"] = "mock"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str | None = None

    email_provider: Literal["mock", "smtp"] = "mock"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str | None = None

    storage_provider: Literal["mock", "cloudinary"] = "mock"
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None

    max_upload_bytes: int = 5 * 1024 * 1024

    @model_validator(mode="after")
    def validate_production_secret(self) -> "Settings":
        if self.app_env == "production" and self.secret_key == "development-only-change-me":
            raise ValueError("SECRET_KEY must be configured in production")
        if self.app_env == "production" and self.database_backend == "memory":
            raise ValueError("In-memory persistence is not allowed in production")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [self.frontend_url.rstrip("/")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
