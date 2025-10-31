from typing import Optional, Dict, Any
from lpm_kernel.api.services.user_llm_config_service import UserLLMConfigService
from openai import OpenAI

class ExpertLLMService:
    """Service for managing expert LLM client"""

    def __init__(self):
        self._client = None
        self.user_llm_config_service = UserLLMConfigService()

    @property
    def client(self) -> OpenAI:
        """Get the OpenAI client for expert LLM"""
        if self._client is None:
            self.user_llm_config = self.user_llm_config_service.get_available_llm()
            self._client = OpenAI(api_key=self.user_llm_config.chat_api_key, base_url=self.user_llm_config.chat_endpoint)
        return self._client

    def get_model_params(self) -> Dict[str, Any]:
        """
        Get model specific parameters for expert LLM

        Returns:
            Dict containing model specific parameters
        """
        return {'model': self.user_llm_config.chat_model_name, 'response_format': {'type': 'text'}, 'seed': 42, 'tools': None, 'tool_choice': None}