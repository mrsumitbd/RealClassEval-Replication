from typing import Dict, List
import os


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    _MODEL_ENV_MAPPING: Dict[str, Dict[str, str]] = {
        "openai": {"api_key_var": "OPENAI_API_KEY", "base_url_var": "OPENAI_BASE_URL"},
        "azure_openai": {"api_key_var": "AZURE_OPENAI_API_KEY", "base_url_var": "AZURE_OPENAI_BASE_URL"},
        "anthropic": {"api_key_var": "ANTHROPIC_API_KEY", "base_url_var": "ANTHROPIC_BASE_URL"},
        "groq": {"api_key_var": "GROQ_API_KEY", "base_url_var": "GROQ_BASE_URL"},
        "together": {"api_key_var": "TOGETHER_API_KEY", "base_url_var": "TOGETHER_BASE_URL"},
        "deepseek": {"api_key_var": "DEEPSEEK_API_KEY", "base_url_var": "DEEPSEEK_BASE_URL"},
        "google": {"api_key_var": "GOOGLE_API_KEY", "base_url_var": "GOOGLE_API_BASE_URL"},
    }

    def __init__(self, model_name: str):
        model_info = self._get_model_info(model_name)
        self.model_name: str = model_info["model_name"]
        self.api_key: str = model_info["api_key"]
        self.base_url: str = model_info["base_url"]
        self.api_key_var: str = model_info["api_key_var"]
        self.base_url_var: str = model_info["base_url_var"]

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        normalized_name = (model_name or "").strip().lower()
        env_mapping = self._MODEL_ENV_MAPPING.get(normalized_name)

        if env_mapping is None:
            env_mapping = self._MODEL_ENV_MAPPING["openai"]
            normalized_name = "openai"

        api_key_var = env_mapping["api_key_var"]
        base_url_var = env_mapping["base_url_var"]

        api_key = os.getenv(api_key_var, "") or ""
        base_url = os.getenv(base_url_var, "") or ""

        return {
            "model_name": normalized_name,
            "api_key": api_key,
            "base_url": base_url,
            "api_key_var": api_key_var,
            "base_url_var": base_url_var,
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return sorted(cls._MODEL_ENV_MAPPING.keys())
