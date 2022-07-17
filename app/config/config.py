import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    admin_username: str = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password: str = os.environ.get("ADMIN_PASSWORD", "admin")
    offer_token: str | None = os.environ.get("OFFER_TOKEN")
    offer_url: str | None = os.environ.get("OFFER_URL")
    secret_key: str = os.environ.get("SECRET_KEY", "123456789")
    db_url: str = os.environ.get("DB_URL", "sqlite:///database.db")
    offer_refresh_rate_sec: int = Field(
        default=os.environ.get("OFFER_REFRESH_RATE_SEC", 300)
    )
    jwt_expiration_time_min: int = Field(
        default=os.environ.get("JWT_EXPIRATION_TIME_MIN", 5)
    )


settings = Settings()
