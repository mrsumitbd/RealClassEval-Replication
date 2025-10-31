
import os
from typing import Dict, List


class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """

    # Mapping of supported model names to their environment variable prefixes
    _MODEL_ENV_MAP: Dict[str, str] = {
        "gpt-4o": "OPENAI",
        "gpt-4o-mini": "OPENAI",
        "deepseek-chat": "DEEPSEEK",
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
        prefix = self._MODEL_ENV_MAP.get(model_name)
        if prefix:
            api_key_var = f"{prefix}_API_KEY"
            base_url_var = f"{prefix}_BASE_URL"
            api_key = os.getenv(api_key_var)
            base_url = os.getenv(base_url_var)
            if not api_key or not base_url:
                raise ValueError(
                    f"Missing environment variables for {model_name}: "
                    f"{api_key_var} and {base_url_var} must be set."
                )
            return {"api_key": api_key, "base_url": base_url}
        else:
            # Default to OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            if not api_key or not base_url:
                raise ValueError(
                    "Missing environment variables for default OpenAI configuration: "
                    "OPENAI_API_KEY and OPENAI_BASE_URL must be set."
                )
            return {"api_key": api_key, "base_url": base_url}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return list(cls._MODEL_ENV_MAP.keys())
