
import os
from typing import Dict, List


class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """

    # Mapping of supported models to the environment variable names that hold
    # their API key and base URL.
    _MODEL_ENV_MAP: Dict[str, Dict[str, str]] = {
        "gpt-4o": {"api_key_env": "OPENAI_API_KEY", "base_url_env": "OPENAI_BASE_URL"},
        "gpt-4o-mini": {"api_key_env": "OPENAI_API_KEY", "base_url_env": "OPENAI_BASE_URL"},
        "deepseek-chat": {"api_key_env": "DEEPSEEK_API_KEY", "base_url_env": "DEEPSEEK_BASE_URL"},
        # Add more models here as needed.
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
        info = self._get_model_info(model_name)
        self.api_key = info["api_key"]
        self.base_url = info["base_url"]

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        """
        if model_name in self._MODEL_ENV_MAP:
            env_map = self._MODEL_ENV_MAP[model_name]
            api_key = os.getenv(env_map["api_key_env"])
            base_url = os.getenv(env_map["base_url_env"])
            if not api_key or not base_url:
                raise ValueError(
                    f"Missing environment variables for model '{model_name}'. "
                    f"Expected '{env_map['api_key_env']}' and '{env_map['base_url_env']}'."
                )
            return {"api_key": api_key, "base_url": base_url}
        else:
            # Default to OpenAI environment variables
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            if not api_key or not base_url:
                raise ValueError(
                    "Missing OpenAI environment variables 'OPENAI_API_KEY' and/or 'OPENAI_BASE_URL'."
                )
            return {"api_key": api_key, "base_url": base_url}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return list(cls._MODEL_ENV_MAP.keys())
