
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    SUPPORTED_MODELS = ['gpt-4o', 'deepseek-chat']

    def __init__(self, model_name: str):
        '''
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        '''
        if model_name not in self.get_supported_models():
            raise ValueError(
                f"Model '{model_name}' is not supported. Supported models: {self.get_supported_models()}")

        self.model_info = self._get_model_info(model_name)
        self.api_key = self.model_info.get('api_key')
        self.base_url = self.model_info.get('base_url')

        if not self.api_key or not self.base_url:
            raise ValueError(
                "Environment variables for API key or base URL are missing.")

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        if model_name == 'gpt-4o':
            return {
                'api_key': os.getenv('GPT4O_API_KEY'),
                'base_url': os.getenv('GPT4O_BASE_URL')
            }
        elif model_name == 'deepseek-chat':
            return {
                'api_key': os.getenv('DEEPSEEK_CHAT_API_KEY'),
                'base_url': os.getenv('DEEPSEEK_CHAT_BASE_URL')
            }
        else:
            return {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'base_url': os.getenv('OPENAI_BASE_URL')
            }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return cls.SUPPORTED_MODELS
