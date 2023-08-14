import base64
import json
import logging.config
import time
from os import path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), 'logging.ini'),
    disable_existing_loggers=False
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# API instantiation
app = FastAPI(title="mloh-sandbox")


# Health check endpoint to determine if the service is up and running
@app.get("/health")
async def health_check():
    """Health check response"""
    return {"Hello": "World"}
