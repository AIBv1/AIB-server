from unittest import mock
from src.services.chat_service import ChatService


@mock.patch("src.integrations.chatgpt_integration.ChatGPTIntegration.generate_response", return_value="Mock response")
def test_get_chat_response(self):
    # Mock the OpenAIIntegration generate_text method
    chat_service = ChatService()
    response = chat_service.get_chat_response("Hello")
    print(response)
    assert response == "Mock response"
