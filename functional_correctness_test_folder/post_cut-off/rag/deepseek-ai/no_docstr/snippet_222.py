
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    def __init__(self, model_name: str):
        '''
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        '''
        self.model_name = model_name
        model_info = self._get_model_info(model_name)

        self.base_url = os.getenv(model_info.get(
            'base_url_env', 'OPENAI_BASE_URL'))
        self.api_key = os.getenv(model_info.get(
            'api_key_env', 'OPENAI_API_KEY'))

        if not self.base_url or not self.api_key:
            raise ValueError(
                f"Missing environment variables for model {model_name}")

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        supported_models = {
            'gpt-4o': {
                'base_url_env': 'OPENAI_BASE_URL',
                'api_key_env': 'OPENAI_API_KEY'
            },
            'deepseek-chat': {
                'base_url_env': 'DEEPSEEK_BASE_URL',
                'api_key_env': 'DEEPSEEK_API_KEY'
            }
        }
        return supported_models.get(model_name, {})

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return ['gpt-4o', 'deepseek-chat']
