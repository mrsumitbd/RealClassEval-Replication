
import os
from typing import Dict, List


class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """

    # Mapping of supported model names to the environment variable names
    # that hold the API key and base URL for that model.
    _MODEL_ENV_MAP: Dict[str, Dict[str, str]] = {
        # OpenAI models
        "gpt-4": {"api_key": "OPENAI_API_KEY", "base_url": "OPENAI_BASE_URL"},
        "gpt-3.5-turbo": {"api_key": "OPENAI_API_KEY", "base_url": "OPENAI_BASE_URL"},
        # Anthropic
        "claude-3-opus-20240229": {"api_key": "ANTHROPIC_API_KEY", "base_url": "ANTHROPIC_BASE_URL"},
        # Cohere
        "command": {"api_key": "COHERE_API_KEY", "base_url": "COHERE_BASE_URL"},
    }

    def __init__(self, model_name: str):
        """
        Initialize the configuration for the given model name.
        Raises ValueError if required environment variables are missing.
        """
        self.model_name = model_name
        config = self._get_model_info(model_name)
        self.api_key = config["api_key"]
        self.base_url = config["base_url"]

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        """
        env_map = self._MODEL_ENV_MAP.get(
            model_name,
            {"api_key": "OPENAI_API_KEY", "base_url": "OPENAI_BASE_URL"},
        )

        api_key = os.getenv(env_map["api_key"])
        base_url = os.getenv(env_map["base_url"])

        if api_key is None:
            raise ValueError(
                f"Missing required environment variable '{env_map['api_key']}' for model '{model_name}'."
            )
        if base_url is None:
            raise ValueError(
                f"Missing required environment variable '{env_map['base_url']}' for model '{model_name}'."
            )

        return {"api_key": api_key, "base_url": base_url}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return list(cls._MODEL_ENV_MAP.keys())
