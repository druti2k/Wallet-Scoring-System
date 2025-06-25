from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pydantic import field_validator

class Settings(BaseSettings):
    # Application
    app_name: str = "Wallet Scoring System"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com"
    ]
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                import json
                return json.loads(v)
            return [i.strip() for i in v.split(",") if i.strip()]
        return v
    
    # Database
    database_url: str = "postgresql://user:password@localhost/wallet_scoring"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # API Keys
    openai_api_key: Optional[str] = None
    etherscan_api_key: Optional[str] = None
    alchemy_api_key: Optional[str] = None
    the_graph_api_key: Optional[str] = None
    
    # RPC URLs
    ethereum_rpc_url: str = "https://mainnet.infura.io/v3/your-project-id"
    polygon_rpc_url: str = "https://polygon-rpc.com"
    bsc_rpc_url: str = "https://bsc-dataseed.binance.org"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    prometheus_enabled: bool = True
    
    # ML Models
    model_path: str = "ml/models/"
    cache_ttl: int = 3600  # 1 hour
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are configured"""
    required_keys = [
        "openai_api_key",
        "etherscan_api_key", 
        "alchemy_api_key"
    ]
    
    missing_keys = []
    for key in required_keys:
        if not getattr(settings, key):
            missing_keys.append(key)
    
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")

# Validate on import
if settings.environment == "production":
    validate_settings() 