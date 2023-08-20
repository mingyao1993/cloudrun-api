import logging.config
import time
from os import path

from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response

from cloud.datastore import data_store
from cloud.pubsub import decode_pubsub_data
from model.pubsub import PubSubRequest

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
def health_check():
    """Health check response"""
    logger.info("health check endpoint")
    return {"health": "ok"}


@app.post("/v1/transfer_funds", response_model=dict)
def update_datastore(request: PubSubRequest):
    decoded_data = decode_pubsub_data(request.message.data)
    data_store.transfer_funds(from_account=decoded_data['from'], to_account=decoded_data['to'],
                              amount=decoded_data['amount'])
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({"message": "success"}))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.middleware("http")
async def api_middleware(request: Request, call_next):
    # Count request time performance
    start_time = time.perf_counter()
    response = await call_next(request)
    body = b""
    async for data in response.body_iterator:
        body += data
    process_time_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"Processing Stats (Request:{request.scope['path']}---Time:{process_time_ms:.1f} milliseconds---",
        {"httpStatusCode": response.status_code},
    )
    # Send back a new Response object. Required because the body was extracted for logging
    return Response(
        content=body, status_code=response.status_code, headers=response.headers
    )
