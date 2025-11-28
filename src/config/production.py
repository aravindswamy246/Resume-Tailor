"""
Production-specific settings and validation
"""
import os
from typing import List, Optional


class ProductionSettings:
    """Production-specific settings"""

    # Required environment variables
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Optional with defaults
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Render-specific
    PORT: int = int(os.getenv("PORT", "8000"))
    RENDER: bool = os.getenv("RENDER", "").lower() == "true"

    # Security
    ALLOWED_HOSTS: List[str] = [host.strip() for host in os.getenv(
        "ALLOWED_HOSTS", "").split(",") if host.strip()]

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        if not cls.OPENAI_API_KEY.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")

        return True

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.RENDER or os.getenv("ENV") == "production"
