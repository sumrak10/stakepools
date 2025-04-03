from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TRONGRID_",
        extra="ignore",
    )

    API_KEY: str
    BASE_URL: str
    LONG_POOLING_RPM_FREQ: int = 1


trongrid_settings = Settings()
