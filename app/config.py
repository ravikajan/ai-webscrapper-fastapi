from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    # Basic API settings
    PROJECT_NAME: str = "FastAPI Scraper"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A web scraping API using FastAPI and ScraperGraph-AI"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 1
    
    # Security settings (for future use)
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
    ]
    
    # Database settings (for future use)
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # API folder path
    API_FOLDER: Path = Path(__file__).parent / "api"

    # ScraperGraph-AI settings
    SCRAPERGRAPH_API_KEY: str = "your-api-key-here"
    SCRAPERGRAPH_API_URL: str = "https://api.scrapergraph.com/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()