from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "Customer Service API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = "sqlite:///./customer_service.db"

    # OpenTelemetry settings
    OTEL_SERVICE_NAME: str = "customer-service"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # Cors settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost", "http://localhost:8080", "https://localhost",
                                       "https://localhost:8080"]

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"  # In production, use a proper secret key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Optional: Cloud provider settings (for future use)
    CLOUD_PROVIDER: Optional[str] = None
    CLOUD_REGION: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()