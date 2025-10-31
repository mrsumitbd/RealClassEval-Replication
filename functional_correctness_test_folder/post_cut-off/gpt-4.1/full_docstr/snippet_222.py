
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    # Supported models and their environment variable mappings
    _MODEL_ENV_MAP = {
        'gpt-4o': {
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY'
        },
        'gpt-3.5-turbo': {
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY'
        },
        'deepseek-chat': {
            'base_url_env': 'DEEPSEEK_BASE_URL',
            'api_key_env': 'DEEPSEEK_API_KEY'
        },
        'deepseek-coder': {
            'base_url_env': 'DEEPSEEK_BASE_URL',
            'api_key_env': 'DEEPSEEK_API_KEY'
        },
        'gemini-pro': {
            'base_url_env': 'GEMINI_BASE_URL',
            'api_key_env': 'GEMINI_API_KEY'
        }
    }

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
        self.base_url = model_info['base_url']
        self.api_key = model_info['api_key']

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        env_map = self._MODEL_ENV_MAP.get(model_name, {
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY'
        })
        base_url = os.environ.get(env_map['base_url_env'])
        api_key = os.environ.get(env_map['api_key_env'])
        if base_url is None or api_key is None:
            raise ValueError(
                f"Missing environment variable(s) for model '{model_name}': "
                f"{env_map['base_url_env']} or {env_map['api_key_env']}"
            )
        return {'base_url': base_url, 'api_key': api_key}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return list(cls._MODEL_ENV_MAP.keys())
