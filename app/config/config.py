import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    admin_username: str = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password: str = os.environ.get("ADMIN_PASSWORD", "admin")
    offer_token: str | None = os.environ.get(
        "OFFER_TOKEN", "c1287585-083c-4250-99dd-72d9f413106d"
    )
    offer_url: str | None = os.environ.get(
        "OFFER_URL",
        "https://applifting-python-excercise-ms.herokuapp.com/api/v1",
    )
    secret_key: str = os.environ.get("SECRET_KEY", "123456789")
    db_url: str = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    offer_refresh_rate_sec: int = Field(
        default=os.environ.get("OFFER_REFRESH_RATE_SEC", 60)
    )
    jwt_expiration_time_min: int = Field(
        default=os.environ.get("JWT_EXPIRATION_TIME_MIN", 5)
    )


settings = Settings()
