from __future__ import annotations
import sys
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        extra="ignore",
    )

    USER: str
    PASS: str
    HOST: str
    PORT: int
    NAME: str

    POOL_SIZE: int = 30
    MAX_POOL_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 10

    @property
    def DSN(self) -> str:  # noqa: N802
        return (f"postgresql+asyncpg://"
                f"{self.USER}:{quote_plus(self.PASS)}"
                f"@{self.HOST}:{self.PORT}/{self.NAME}")


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="test.env",
        env_prefix="DB_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings | TestSettings:
    if "pytest" in sys.modules:
        return TestSettings()
    return Settings()
