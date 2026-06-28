# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Central configuration loaded from environment variables / .env file.

    pydantic-settings automatically reads from the environment and .env file.
    @lru_cache ensures we only parse the config once — not on every import.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Application
    app_name: str = "AI Chatbot"
    app_env: str = "development"
    debug: bool = True

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "chatbot_db"
    postgres_user: str = "chatbot_user"
    postgres_password: str = "chatbot_pass"

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    @property
    def database_url(self) -> str:
        """
        Builds the SQLAlchemy connection string dynamically.
        Format: postgresql+psycopg://user:password@host:port/database
        We use 'psycopg' (version 3) as the driver.
        """
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached singleton of Settings.
    Use this everywhere instead of instantiating Settings() directly.
    """
    return Settings()