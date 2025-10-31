import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    _PROVIDERS: Dict[str, Dict[str, object]] = {
        'openai': {
            'models': {
                'gpt-4o',
                'gpt-4o-mini',
                'gpt-4.1',
                'gpt-4.1-mini',
                'o3-mini',
                'o4-mini',
            },
            'base_url_env': 'OPENAI_BASE_URL',
            'api_key_env': 'OPENAI_API_KEY',
        },
        'deepseek': {
            'models': {
                'deepseek-chat',
                'deepseek-reasoner',
            },
            'base_url_env': 'DEEPSEEK_BASE_URL',
            'api_key_env': 'DEEPSEEK_API_KEY',
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
        if not isinstance(model_name, str) or not model_name.strip():
            raise ValueError("model_name must be a non-empty string")

        self.model_name = model_name
        info = self._get_model_info(model_name)

        base_url = info.get('base_url')
        api_key = info.get('api_key')

        if not api_key:
            raise ValueError(
                f"API key not found in environment for model '{model_name}' (expected env: {info.get('api_key_env')})")
        if not base_url:
            raise ValueError(
                f"Base URL not found in environment for model '{model_name}' (expected env: {info.get('base_url_env')})")

        self.base_url = base_url
        self.api_key = api_key
        self.provider = info.get('provider', 'openai')
        self.api_key_env = info.get('api_key_env')
        self.base_url_env = info.get('base_url_env')

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        provider = None
        for prov, cfg in self._PROVIDERS.items():
            if model_name in cfg.get('models', set()):
                provider = prov
                base_url_env = cfg['base_url_env']
                api_key_env = cfg['api_key_env']
                break

        # Default to OpenAI env vars if model is not recognized
        if provider is None:
            provider = 'openai'
            base_url_env = self._PROVIDERS['openai']['base_url_env']
            api_key_env = self._PROVIDERS['openai']['api_key_env']

        base_url = os.getenv(base_url_env)
        api_key = os.getenv(api_key_env)

        return {
            'provider': provider,
            'base_url_env': base_url_env,
            'api_key_env': api_key_env,
            'base_url': base_url,
            'api_key': api_key,
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        models: List[str] = []
        for cfg in cls._PROVIDERS.values():
            models.extend(sorted(list(cfg.get('models', set()))))
        return sorted(models)
