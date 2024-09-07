from fastapi import FastAPI
from app.api import customers
from app.core.config import settings
from app.core.logging import setup_logging
from app.utils.telemetry import setup_telemetry
from app.database import init_db
from app.models import database as db_models

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A cloud-native customer service API"
)

# Initialize database
init_db()

# Setup logging
setup_logging()

# Setup telemetry
setup_telemetry(app)

# Include routers
app.include_router(customers.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Customer Service API",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

