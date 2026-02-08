"""
HackMate v2.0 - Configuration Module
Loads environment variables and provides app settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Info
    app_name: str = "HackMate v2.0"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "sqlite:///./hackmate.db"
    
    # Security
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # AI (Google Gemini)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 2048
    
    # Terminal
    command_timeout: int = 300  # 5 minutes
    max_commands_per_minute: int = 10
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
