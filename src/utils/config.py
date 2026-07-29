from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    environment: str = "development"
    log_level: str = "INFO"
    mlflow_tracking_uri: str = "http://localhost:5000"

    @property
    def database_url(self) -> str:
        return "postgresql+asyncpg://mluser:mlpassword@localhost:5432/ml_db"

@lru_cache
def get_settings() -> Settings:
    return Settings()
