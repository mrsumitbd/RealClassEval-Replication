
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    SUPPORTED_MODELS = {
        'gpt-4o': {'base_url': 'https://api.example.com/gpt-4o', 'api_key_env': 'GPT4O_API_KEY'},
        'deepseek-chat': {'base_url': 'https://api.example.com/deepseek-chat', 'api_key_env': 'DEEPSEEK_CHAT_API_KEY'}
    }

    def __init__(self, model_name: str):
        '''
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        '''
        model_info = self._get_model_info(model_name)
        self.base_url = model_info['base_url']
        self.api_key = os.getenv(model_info['api_key_env'])
        if not self.api_key:
            raise ValueError(
                f"Environment variable {model_info['api_key_env']} is missing for model {model_name}.")

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        return self.SUPPORTED_MODELS.get(model_name, {'base_url': os.getenv('OPENAI_BASE_URL'), 'api_key_env': 'OPENAI_API_KEY'})

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return list(cls.SUPPORTED_MODELS.keys())
