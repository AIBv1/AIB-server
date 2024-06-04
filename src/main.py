import logging
import time
from fastapi import FastAPI, Request
from .api.v1.endpoints.chat_api import router as chat_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include router
app.include_router(chat_router)

# Middleware for logging and basic monitoring
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Request: {request.method} {request.url} - Completed in {process_time}ms - Status code: {response.status_code}")
    return response
