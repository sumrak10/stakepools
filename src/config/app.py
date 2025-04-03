from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvinronmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )

    ENVIRONMENT: EnvinronmentType
    SSL: bool
    HOST: str
    PORT: str

    def get_base_url(self) -> str:
        return f"http{'s' if self.SSL else ''}://{self.HOST}:{self.PORT}"


app_settings = Settings()
