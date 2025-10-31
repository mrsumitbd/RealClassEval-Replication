
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)
        self.api_key = os.getenv(self.model_info['api_key_env_var'])
        self.base_url = os.getenv(self.model_info['base_url_env_var'])

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        model_info_map = {
            'gpt-3.5-turbo': {
                'api_key_env_var': 'OPENAI_API_KEY',
                'base_url_env_var': 'OPENAI_BASE_URL'
            },
            'gpt-4': {
                'api_key_env_var': 'OPENAI_API_KEY',
                'base_url_env_var': 'OPENAI_BASE_URL'
            },
            'claude-2': {
                'api_key_env_var': 'ANTHROPIC_API_KEY',
                'base_url_env_var': 'ANTHROPIC_BASE_URL'
            },
            'llama-2': {
                'api_key_env_var': 'META_API_KEY',
                'base_url_env_var': 'META_BASE_URL'
            }
        }
        return model_info_map.get(model_name, {
            'api_key_env_var': 'OPENAI_API_KEY',
            'base_url_env_var': 'OPENAI_BASE_URL'
        })

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return ['gpt-3.5-turbo', 'gpt-4', 'claude-2', 'llama-2']
