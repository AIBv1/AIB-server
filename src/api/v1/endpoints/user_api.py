from datetime import timedelta, datetime
from http.client import HTTPException
from typing import Optional

import httpx
from fastapi import FastAPI, Request, Depends
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.dtos.refresh_token_request import TokenRefreshRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


from src.database.model import SNSType
from src.services.user_service import UserService, MySqlService

router = APIRouter()
user_service = UserService()
mysql_service = MySqlService()
def get_mysql_service():
    return

def get_user_service():
    return user_service

KAKAO_CLIENT_ID = "d79713dd6f4e3b0f92c1d514b57965e2"
KAKAO_CLIENT_SECRET = "TjnTVGUhF5zWkHdSxgkijcRESqZEXIga"
# KAKAO_REDIRECT_URI = "http://localhost:8000/api/auth/kakao/callback"
KAKAO_REDIRECT_URI = "http://100.27.81.247/api/auth/kakao/callback"



KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

SECRET_KEY = "temp_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =60 * 24
REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.get("/api/users/login/kakao")
async def kakao_login():

    kakao_login_url = (
        f"{KAKAO_AUTH_URL}?client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
        f"&scope=account_email"
    )

    return RedirectResponse(url = kakao_login_url)

@router.get("/api/auth/kakao/callback")
async def kakao_callback(request: Request, user_service: UserService = Depends(get_user_service)):
    code = request.query_params.get("code")

    if code is None:
        return {"error": "No code provided"}

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            KAKAO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_CLIENT_ID,
                "client_secret": KAKAO_CLIENT_SECRET,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "code": code,
            },
        )

        token_response_json = token_response.json()
        access_token = token_response_json.get("access_token")


        if access_token is None:
            return {"error": "Failed to retrieve access token"}

        user_info_response = await client.get(
            KAKAO_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
    user_info = user_info_response.json()
    kakao_account = user_info.get("kakao_account", {})
    email = kakao_account.get("email")
    profile = kakao_account.get("profile", {})
    username = profile.get("nickname")
    profile_image = profile.get("profile_image_url")

    user = await user_service.get_or_create_user(email=email, username=username, sns_type=SNSType.KAKAO, profile_image_url=profile_image)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


@router.post("/api/users/token/refresh")
async def refresh_token(request: TokenRefreshRequest):
    try:
        refresh_token = request.refresh_token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        new_refresh_token = create_refresh_token(data={"sub": email}, expires_delta=refresh_token_expires)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/api/users/me")
async def read_users_me(request: Request, mysql_service: MySqlService = Depends(get_mysql_service())):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    return await mysql_service.get_user_by_email(email=request.state.user)
