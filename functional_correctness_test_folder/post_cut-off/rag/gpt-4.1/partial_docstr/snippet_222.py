import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    _MODEL_ENV_MAP = {
        'gpt-4o': {
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY'
        },
        'gpt-4': {
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
        'claude-3-opus': {
            'base_url_env': 'ANTHROPIC_BASE_URL',
            'api_key_env': 'ANTHROPIC_API_KEY'
        },
        'claude-3-sonnet': {
            'base_url_env': 'ANTHROPIC_BASE_URL',
            'api_key_env': 'ANTHROPIC_API_KEY'
        },
        'claude-3-haiku': {
            'base_url_env': 'ANTHROPIC_BASE_URL',
            'api_key_env': 'ANTHROPIC_API_KEY'
        },
        'gemini-pro': {
            'base_url_env': 'GOOGLE_BASE_URL',
            'api_key_env': 'GOOGLE_API_KEY'
        },
        'gemini-1.5-pro': {
            'base_url_env': 'GOOGLE_BASE_URL',
            'api_key_env': 'GOOGLE_API_KEY'
        },
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
        info = self._get_model_info(model_name)
        self.base_url = info.get('base_url')
        self.api_key = info.get('api_key')

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        env_map = self._MODEL_ENV_MAP.get(model_name)
        if env_map is None:
            # Default to OpenAI
            base_url_env = 'OPENAI_BASE_URL'
            api_key_env = 'OPENAI_API_KEY'
        else:
            base_url_env = env_map['base_url_env']
            api_key_env = env_map['api_key_env']

        base_url = os.environ.get(base_url_env)
        api_key = os.environ.get(api_key_env)

        if not base_url or not api_key:
            raise ValueError(
                f"Missing environment variable(s) for model '{model_name}': "
                f"{base_url_env if not base_url else ''} "
                f"{api_key_env if not api_key else ''}"
            )

        return {
            'base_url': base_url,
            'api_key': api_key
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return list(cls._MODEL_ENV_MAP.keys())
