from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # AI API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str

    # Database
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    # AI Models
    PLANNER_MODEL: str = "gpt-4o"
    ARCHITECT_MODEL: str = "claude-sonnet-3.5"
    CODEGEN_MODEL: str = "gpt-4o"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
