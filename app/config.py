"""
Configuration de l'application
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    app_name: str = "Aula Calendar Manager"
    secret_key: str = "your-secret-key-here"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Base de donn?es
    database_url: str = "sqlite:///./aula_calendar.db"
    
    # Google Calendar API
    google_client_id: str = ""
    google_client_secret: str = ""
    
    # Aula Configuration
    aula_base_url: str = "https://www.aula.dk"
    aula_api_version: str = "v19"
    
    # Redis (optionnel)
    redis_url: Optional[str] = None
    cache_ttl: int = 300
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/aula_calendar.log"
    
    # Email notifications (optionnel)
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None
    
    # Webhooks (optionnel)
    slack_webhook_url: Optional[str] = None
    discord_webhook_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()