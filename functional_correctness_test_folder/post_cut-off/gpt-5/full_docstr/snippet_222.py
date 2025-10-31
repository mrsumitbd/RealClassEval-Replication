from typing import Dict, List
import os


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    _PROVIDERS: Dict[str, Dict[str, str]] = {
        "openai": {"api_key_env": "OPENAI_API_KEY", "base_url_env": "OPENAI_BASE_URL"},
        "deepseek": {"api_key_env": "DEEPSEEK_API_KEY", "base_url_env": "DEEPSEEK_BASE_URL"},
        "anthropic": {"api_key_env": "ANTHROPIC_API_KEY", "base_url_env": "ANTHROPIC_BASE_URL"},
    }

    _MODEL_PROVIDER_MAP: Dict[str, str] = {
        # OpenAI
        "gpt-4o": "openai",
        "gpt-4o-mini": "openai",
        "o4-mini": "openai",
        "gpt-4.1": "openai",
        "gpt-4.1-mini": "openai",
        # DeepSeek
        "deepseek-chat": "deepseek",
        "deepseek-reasoner": "deepseek",
        # Anthropic
        "claude-3.5-sonnet": "anthropic",
        "claude-3.5-haiku": "anthropic",
    }

    def __init__(self, model_name: str):
        '''
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        '''
        if model_name not in self._MODEL_PROVIDER_MAP:
            raise ValueError(
                f"Unsupported model: {model_name}. Supported models: {', '.join(self.get_supported_models())}"
            )

        info = self._get_model_info(model_name)
        api_key_env = info["api_key_env"]
        base_url_env = info["base_url_env"]

        api_key = os.getenv(api_key_env)
        base_url = os.getenv(base_url_env)

        missing = []
        if not api_key:
            missing.append(api_key_env)
        if not base_url:
            missing.append(base_url_env)

        if missing:
            raise ValueError(
                f"Missing required environment variable(s): {', '.join(missing)} for provider '{info['provider']}'"
            )

        self.model_name: str = model_name
        self.provider: str = info["provider"]
        self.api_key: str = api_key  # type: ignore[assignment]
        self.base_url: str = base_url  # type: ignore[assignment]

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        provider = self._MODEL_PROVIDER_MAP.get(model_name)
        if provider is None:
            provider = "openai"
        envs = self._PROVIDERS[provider]
        return {
            "provider": provider,
            "api_key_env": envs["api_key_env"],
            "base_url_env": envs["base_url_env"],
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return sorted(cls._MODEL_PROVIDER_MAP.keys())
