from typing import Annotated
from fastapi import Depends, Request
from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from urllib.parse import urlparse


class AppSettings(BaseSettings):
    name: str = "Board API"
    debug: bool = False


class AuthSettings(BaseSettings):
    secret: str
    expired_time: int


class DatabaseSettings(BaseSettings):
    url: str
    url_sync: str


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str
    database_url_sync: str
    jwt_secret: str
    jwt_expired_time: int

    @property
    def app(self) -> AppSettings:
        return AppSettings()

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url, url_sync=self.database_url_sync)

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(secret=self.jwt_secret, expired_time=self.jwt_expired_time)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        parsed = urlparse(v)

        dbname = parsed.path.lstrip("/") or ""

        if parsed.scheme not in ["postgresql", "postgresql+asyncpg", "sqlite"]:
            raise ValueError("DATABASE_URL must start with postgresql:// or sqlite://")

        if not parsed.hostname:
            raise ValueError("DATABASE_URL must contain a host")

        if not dbname:
            raise ValueError("DATABASE_URL must contain a database name")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("DATABASE_URL must contain a valid port")

        return v


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
