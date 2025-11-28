"""
Configuration management for Resume Tailor application.
Centralized settings for production deployment.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Application
    APP_NAME: str = "Resume Tailor"
    APP_VERSION: str = "0.1.1"
    DEBUG: bool = False
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # OpenAI
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: Path = Path(__file__).parent.parent.parent / "logs"
    
    # File Storage
    DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"
    INPUT_DIR: Path = DATA_DIR / "input"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    
    # Security
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
