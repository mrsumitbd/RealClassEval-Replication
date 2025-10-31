
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
        self.model_info = self._get_model_info(model_name)
        self.api_key = os.getenv(self.model_info['api_key_env_var'])
        self.base_url = os.getenv(self.model_info['base_url_env_var'])

        if not self.api_key or not self.base_url:
            raise ValueError(
                f"Missing environment variables for model {model_name}")

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        model_configs = {
            'gpt-4o': {
                'api_key_env_var': 'OPENAI_API_KEY',
                'base_url_env_var': 'OPENAI_BASE_URL'
            },
            'deepseek-chat': {
                'api_key_env_var': 'DEEPSEEK_API_KEY',
                'base_url_env_var': 'DEEPSEEK_BASE_URL'
            }
        }

        return model_configs.get(model_name, {
            'api_key_env_var': 'OPENAI_API_KEY',
            'base_url_env_var': 'OPENAI_BASE_URL'
        })

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return ['gpt-4o', 'deepseek-chat']
