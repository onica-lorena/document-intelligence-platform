from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Document Intelligence Platform API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    MONGODB_URL: str
    DATABASE_NAME: str

    STORAGE_PATH: str

    QDRANT_URL: str
    QDRANT_COLLECTION: str

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:8b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()