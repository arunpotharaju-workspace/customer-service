from fastapi import FastAPI
from app.api import customers
from app.core.config import settings
from app.core.logging import setup_logging
from app.utils.telemetry import setup_telemetry
from app.database import init_db

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

setup_logging()
setup_telemetry(app)

# Initialize database
init_db()

# Include routers
app.include_router(customers.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Customer Service API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)