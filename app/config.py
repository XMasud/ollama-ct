from pydantic import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Local AI Service"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3.5"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")