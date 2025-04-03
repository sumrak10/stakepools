from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BLOCKCHAIN_",
        extra="ignore",
    )

    TRC20_ADDRESS: str


blockchain_settings = Settings()
