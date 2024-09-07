from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api import customers
from app.core.config import settings
from app.core.logging import logger
from app.utils.telemetry import setup_telemetry
from app.database import init_db
from app.core.auth import create_access_token, verify_token

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A cloud-native customer service API"
)

# Initialize database
init_db()

# Setup telemetry
setup_telemetry(app)

# Include routers
app.include_router(customers.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_token)])

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("Login attempt", privacy_level="MEDIUM", username=form_data.username)
    # In a real application, you would verify the username and password against a database
    if form_data.username != "test" or form_data.password != "test":
        logger.warning("Failed login attempt", privacy_level="MEDIUM", username=form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    logger.info("Successful login", privacy_level="MEDIUM", username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    logger.info("Root endpoint accessed", privacy_level="LOW")
    return {
        "message": "Welcome to the Customer Service API",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed", privacy_level="LOW")
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Customer Service API", privacy_level="LOW")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Customer Service API", privacy_level="LOW")