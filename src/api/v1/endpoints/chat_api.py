from fastapi import APIRouter
from src.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

@router.post("/v1/chat")
async def chat_with_llm(message: str):
    return {"response": chat_service.get_chat_response(message)}
