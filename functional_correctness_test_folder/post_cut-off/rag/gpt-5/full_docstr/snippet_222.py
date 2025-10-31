from typing import Dict, List
import os


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    # Mapping of providers to their environment variables and supported models
    _PROVIDERS: Dict[str, Dict[str, object]] = {
        'openai': {
            'api_key_env': 'OPENAI_API_KEY',
            'base_url_env': 'OPENAI_BASE_URL',
            'models': ['gpt-4o', 'gpt-4o-mini'],
        },
        'deepseek': {
            'api_key_env': 'DEEPSEEK_API_KEY',
            'base_url_env': 'DEEPSEEK_BASE_URL',
            'models': ['deepseek-chat', 'deepseek-reasoner'],
        },
        'anthropic': {
            'api_key_env': 'ANTHROPIC_API_KEY',
            'base_url_env': 'ANTHROPIC_BASE_URL',
            'models': ['claude-3-5-sonnet', 'claude-3-5-haiku'],
        },
        'google': {
            'api_key_env': 'GOOGLE_API_KEY',
            'base_url_env': 'GOOGLE_BASE_URL',
            'models': ['gemini-1.5-pro', 'gemini-1.5-flash'],
        },
        'groq': {
            'api_key_env': 'GROQ_API_KEY',
            'base_url_env': 'GROQ_BASE_URL',
            'models': ['llama-3.1-70b', 'mixtral-8x7b'],
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
        api_key_env = info['api_key_env']
        base_url_env = info['base_url_env']

        api_key = os.getenv(api_key_env)
        base_url = os.getenv(base_url_env)

        if not api_key:
            raise ValueError(
                f"Missing environment variable '{api_key_env}' for model '{model_name}'.")
        if not base_url:
            raise ValueError(
                f"Missing environment variable '{base_url_env}' for model '{model_name}'.")

        self.provider = info.get('provider', 'openai')
        self.api_key = api_key
        self.base_url = base_url

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        for provider, cfg in self._PROVIDERS.items():
            models = cfg.get('models', [])
            if model_name in models:
                return {
                    'provider': provider,
                    'api_key_env': cfg['api_key_env'],
                    'base_url_env': cfg['base_url_env'],
                }
        # Default to OpenAI env vars for unsupported models
        openai_cfg = self._PROVIDERS['openai']
        return {
            'provider': 'openai',
            'api_key_env': openai_cfg['api_key_env'],
            'base_url_env': openai_cfg['base_url_env'],
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        models: List[str] = []
        for cfg in cls._PROVIDERS.values():
            models.extend(cfg.get('models', []))
        return models
