import logging.config
from os import path

from fastapi import FastAPI

logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), 'config/logging.ini'),
    disable_existing_loggers=False
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# API instantiation
app = FastAPI(title="mloh-sandbox")


# Health check endpoint to determine if the service is up and running
@app.get("/health")
async def health_check():
    """Health check response"""
    logger.info("health check endpoint")
    return {"health": "ok"}
