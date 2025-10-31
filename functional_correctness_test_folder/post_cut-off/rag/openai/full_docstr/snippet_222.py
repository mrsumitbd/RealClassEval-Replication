
import os
from typing import Dict, List, Tuple


class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """

    # Mapping of supported models to their environment variable names
    _MODEL_ENV_MAP: Dict[str, Tuple[str, str]] = {
        # OpenAI models
        "gpt-4o": ("OPENAI_BASE_URL", "OPENAI_API_KEY"),
        "gpt-4o-mini": ("OPENAI_BASE_URL", "OPENAI_API_KEY"),
        "gpt-4o-mini-2024-07-18": ("OPENAI_BASE_URL", "OPENAI_API_KEY"),
        # DeepSeek models
        "deepseek-chat": ("DEEPSEEK_BASE_URL", "DEEPSEEK_API_KEY"),
        # Anthropic models
        "claude-3-5-sonnet-20240620": ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"),
        "claude-3-5-sonnet-20240620": ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"),
    }

    def __init__(self, model_name: str):
        """
        Initializes the model configuration.
        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').
        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        """
        self.model_name = model_name
        config = self._get_model_info(model_name)
        self.base_url = config["base_url"]
        self.api_key = config["api_key"]

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        """
        env_map = self._MODEL_ENV_MAP.get(model_name)
        if env_map:
            base_url_var, api_key_var = env_map
        else:
            # Default to OpenAI environment variables
            base_url_var, api_key_var = ("OPENAI_BASE_URL", "OPENAI_API_KEY")

        base_url = os.getenv(base_url_var)
        api_key = os.getenv(api_key_var)

        if not base_url:
            raise ValueError(
                f"Environment variable '{base_url_var}' is not set for model '{model_name}'.")
        if not api_key:
            raise ValueError(
                f"Environment variable '{api_key_var}' is not set for model '{model_name}'.")

        return {"base_url": base_url, "api_key": api_key}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return list(cls._MODEL_ENV_MAP.keys())
