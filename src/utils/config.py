from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FRAUD_", env_file=".env")
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+asyncpg://fraud:fraudpass@localhost:5432/fraud_db"
    detection_threshold: float = 0.5
    anomaly_contamination: float = 0.01
    batch_max_size: int = 1000
    log_level: str = "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()
