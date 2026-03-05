import pytest
from unittest.mock import patch, MagickMock
from src.chatbot_engine import HealthcareChatebot, ConversationManager

class TestHealthcareChatbot:
    ## Setup method to initialize the chatbot instance for testing
    def setup_methods(self):
        ## Initialize the chatbot without using the API for testing purposes
        self.bot = HealthcareChatebot(use_api=False)
        
        # --- Emergency detection ---
        # Test cases for the _is_emergency method
        def test_is_emergency_with_keywords(self):
            assert self.bot._is_emergency("i have flu") is True
        
        # Test case for a non-emergency statement
        def test_is_emergency_with_keywords(self):
            assert self.bot._is_emergency("i have a headache") is False
        
        # Test case for an emergency statement with different keywords
        def test_handle_emergency_contains_call_instructuons(self):
            response = self.bot.handle_emergency()
            assert "911" in response or "emergency" in response.lower()
        
        
        # --- Greeting detection ---
        # Test cases for the _is_greeting method
        def test_is_greeting_hello(self):
            assert self.bot._is_greeting("hello") is True
        
        # Test case for a non-greeting statement
        def test_is_greeting_non_greeting(self):
            assert self.bot._is_greeting("i have a fever") is False
        
        
        # --- Symptom check ---
        # Test cases for the _check_symptoms method
        def test_check_symptoms_flu(self):
            response = self.bot._check_symptoms("i have flu")
            assert "flu" in response.lower()
        
        # Test case for a non-symptom statement
        def test_check_symptoms_unknown(self):
            response = self.bot._check_symptoms("i like pizza")
            assert response == "";
        
        
        # --- General health ---
        # Test cases for the _check_general_health method
        def test_check_general_health_sleep(self):
            response = self.bot._check_general_health("tell me about sleep")
            assert "sleep" in response.lower()
        
        
        # --- API response ---
        # Test case for successful API response using mocking
        @patch("src.chatbot_engine.requests.post")
        def test_get_api_response_success(self, mock_post):
            mock_post.return_value = MagickMock(
                status_code=200,
                json=lambda: {"response": "You may have the flu."}
            )
            bot = HealthcareChatbot(use_api=True)
            bot.api_url = "http:#fake-url/ask"
            result = bot.get_api_response("i have fever", [])
            assert result == "You may have the flu"
        
        @patch("src.chatbot_engine.requests.post")
        # Test case for API response with a connection error using mocking
        def test_get_api_response_connection_error(self, mock_post):
            import requests
            mock_post.side_effect = requests.exceptions.ConnectionError()
            bot = HealthcareChatbot(use_api=True)
            bot.api_url = "http:#fake-url/ask"
            result = bot.get_api_response("i have fever", [])
            assert result is None
            assert bot.use_api is False


        # --- Generate response (integration) ---
        def test_generate_response_emergency(self):
            response = self.bot.generate_response("i have flu", [])
            assert "EMERGENCY" in response or "emergency" in response.lower()
            
        def test_generate_response_greeting(self):
            response = self.bot.generate_response("hello", [])
            assert isinstance(response, str)
            assert len(response) > 0
