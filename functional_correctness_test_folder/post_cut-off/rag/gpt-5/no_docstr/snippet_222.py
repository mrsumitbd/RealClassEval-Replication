import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    _MODEL_ENV_MAP: Dict[str, Dict[str, str]] = {
        'gpt-4o': {'base_url_env': 'OPENAI_BASE_URL', 'api_key_env': 'OPENAI_API_KEY'},
        'gpt-4o-mini': {'base_url_env': 'OPENAI_BASE_URL', 'api_key_env': 'OPENAI_API_KEY'},
        'deepseek-chat': {'base_url_env': 'DEEPSEEK_BASE_URL', 'api_key_env': 'DEEPSEEK_API_KEY'},
    }
    _DEFAULT_ENV: Dict[str, str] = {
        'base_url_env': 'OPENAI_BASE_URL', 'api_key_env': 'OPENAI_API_KEY'}

    def __init__(self, model_name: str):
        '''
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        '''
        info = self._get_model_info(model_name)
        base_url_env = info['base_url_env']
        api_key_env = info['api_key_env']

        base_url = os.getenv(base_url_env)
        api_key = os.getenv(api_key_env)

        missing = []
        if not base_url:
            missing.append(base_url_env)
        if not api_key:
            missing.append(api_key_env)

        if missing:
            raise ValueError(
                f"Missing required environment variable(s) for model '{model_name}': {', '.join(missing)}")

        self.model_name = model_name
        self.base_url_env = base_url_env
        self.api_key_env = api_key_env
        self.base_url = base_url
        self.api_key = api_key

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        return self._MODEL_ENV_MAP.get(model_name, self._DEFAULT_ENV)

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return sorted(list(cls._MODEL_ENV_MAP.keys()))
