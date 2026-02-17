"""
Application Configuration
Loads settings from environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from .env file
    """
    # Database
    database_url: str = "sqlite:///./nexus.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret: str = ""
    jwt_expiration_minutes: int = 60
    
    # File Upload
    upload_dir: str = "uploads"
    max_file_size_mb: int = 10
    
    # AI Provider Settings
    ai_provider: str = "openai"  # Options: "openai", "groq", "mock"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500
    
    # Groq
    groq_api_key: Optional[str] = None
    groq_model: str = "llama3-8b-8192"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
