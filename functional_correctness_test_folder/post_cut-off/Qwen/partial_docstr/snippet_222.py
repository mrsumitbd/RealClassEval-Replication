
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''
    SUPPORTED_MODELS = {
        'gpt-3': {'base_url': 'https://api.openai.com/v1', 'api_key': os.getenv('GPT3_API_KEY')},
        'gpt-4': {'base_url': 'https://api.openai.com/v1', 'api_key': os.getenv('GPT4_API_KEY')},
        # Add more models as needed
    }
    DEFAULT_BASE_URL = os.getenv(
        'OPENAI_BASE_URL', 'https://api.openai.com/v1')
    DEFAULT_API_KEY = os.getenv('OPENAI_API_KEY')

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        return self.SUPPORTED_MODELS.get(model_name, {
            'base_url': self.DEFAULT_BASE_URL,
            'api_key': self.DEFAULT_API_KEY
        })

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return list(cls.SUPPORTED_MODELS.keys())
