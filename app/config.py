from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Local AI Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3.5:latest"
    OLLAMA_TIMEOUT: float = 120.0
    OLLAMA_THINK: bool = False
    OLLAMA_NUM_CTX: int = 2048
    OLLAMA_NUM_PREDICT: int = 512

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()