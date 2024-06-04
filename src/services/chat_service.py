import logging

from src.integrations.chatgpt_integration import ChatGPTIntegration
from src.integrations.llama_integration import LlamaIntegration


class ChatService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chatgpt_integration = ChatGPTIntegration()
        self.llama_integration = LlamaIntegration()
    def get_chat_response(self, message):
        self.logger.info(f"Processing message: {message}")
        response = self.llama_integration.generate_response(message)
        return response
