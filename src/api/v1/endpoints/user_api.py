import httpx
from fastapi import FastAPI, Request, Depends
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.services.user_service import UserService
router = APIRouter()
user_service = UserService

KAKAO_CLIENT_ID = "d79713dd6f4e3b0f92c1d514b57965e2"
KAKAO_CLIENT_SECRET = "TjnTVGUhF5zWkHdSxgkijcRESqZEXIga"
KAKAO_REDIRECT_URI = "http://localhost:8000/api/auth/kakao/callback"

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"


@router.get("/api/users/login/kakao")
async def kakao_login():

    kakao_login_url = (

        f"{KAKAO_AUTH_URL}?client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )

    return RedirectResponse(url = kakao_login_url)

@router.get("/api/auth/kakao/callback")
async def kakao_callback(request: Request):
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

    return user_info

