import logging
import time
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from .api.v1.endpoints.chat_api import router as chat_router
from .api.v1.endpoints.hello_api import router as hello_router
from .api.v1.endpoints.user_api import router as user_router

SECRET_KEY = "temp_secret_key"
ALGORITHM = "HS256"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include router
app.include_router(chat_router)
app.include_router(hello_router)
app.include_router(user_router)

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: Optional[list] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request: Request, call_next):
        # 경로가 제외 경로에 포함되어 있으면 다음 호출로 넘김
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        if "authorization" not in request.headers:
            return JSONResponse(status_code=401, content={"message": "Authorization header missing"})

        auth_header = request.headers["authorization"]

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload.get("sub")
        except Exception as e:
            return JSONResponse(status_code=401, content={"message": "Invalid token"})


        response = await call_next(request)
        return response

# 제외할 경로 설정
excluded_paths = ["/api/token", "/api/users/login/kakao", "/api/auth/kakao/callback", "/api/users/token/refresh", "/api/hello"]

app.add_middleware(JWTMiddleware, excluded_paths=excluded_paths)

# Middleware for logging and basic monitoring
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Request: {request.method} {request.url} - Completed in {process_time}ms - Status code: {response.status_code}")
    return response
