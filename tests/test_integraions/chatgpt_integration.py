from unittest import mock

from src.integrations.chatgpt_integration import ChatGPTIntegration

@mock.patch("src.integrations.chatgpt_integration.ChatGPTIntegration.generate_response", return_value="Mock response")
def test_chatgpt_integration(self):
    chatgpt_integration = ChatGPTIntegration()
    response = chatgpt_integration.generate_response("hello")
    assert response == "Mock response"
