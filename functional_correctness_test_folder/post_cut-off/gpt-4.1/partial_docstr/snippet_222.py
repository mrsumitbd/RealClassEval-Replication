
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''
    _MODEL_ENV_MAP = {
        'openai': {
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY'
        },
        'anthropic': {
            'base_url_env': 'ANTHROPIC_BASE_URL',
            'api_key_env': 'ANTHROPIC_API_KEY'
        },
        'google': {
            'base_url_env': 'GOOGLE_BASE_URL',
            'api_key_env': 'GOOGLE_API_KEY'
        }
    }

    def __init__(self, model_name: str):
        self.model_name = model_name
        info = self._get_model_info(model_name)
        self.base_url = info['base_url']
        self.api_key = info['api_key']

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        key = model_name.lower()
        envs = self._MODEL_ENV_MAP.get(key, self._MODEL_ENV_MAP['openai'])
        base_url = os.environ.get(envs['base_url_env'], '')
        api_key = os.environ.get(envs['api_key_env'], '')
        return {'base_url': base_url, 'api_key': api_key}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return list(cls._MODEL_ENV_MAP.keys())
