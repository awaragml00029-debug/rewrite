"""Application configuration."""

from typing import List, Literal
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=53431, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")

    # LLM Configuration
    llm_provider: Literal["openai", "gemini"] = Field(default="openai", env="LLM_PROVIDER")
    llm_api_key: str = Field(env="LLM_API_KEY")
    llm_base_url: str = Field(default="https://api.openai.com/v1", env="LLM_BASE_URL")
    llm_model: str = Field(default="gpt-4", env="LLM_MODEL")

    # JANE API Configuration
    jane_wsdl_url: str = Field(
        default="http://jane.biosemantics.org:8080/JaneServer/services/JaneSOAPServer?wsdl",
        env="JANE_WSDL_URL"
    )
    jane_base_url: str = Field(
        default="http://jane.biosemantics.org/",
        env="JANE_BASE_URL"
    )

    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_enabled: bool = Field(default=False, env="REDIS_ENABLED")

    # CORS Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3003", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )

    # Cache Settings
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    enable_cache: bool = Field(default=True, env="ENABLE_CACHE")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
