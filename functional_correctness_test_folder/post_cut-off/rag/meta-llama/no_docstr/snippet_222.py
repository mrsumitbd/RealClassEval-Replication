
import os
from typing import Dict, List


class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """

    SUPPORTED_MODELS = ['gpt-4o', 'deepseek-chat']

    def __init__(self, model_name: str):
        """
        Initializes the model configuration.

        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').

        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        """
        if model_name not in self.get_supported_models():
            raise ValueError(f"Unsupported model: {model_name}")

        model_info = self._get_model_info(model_name)
        if not model_info['api_key']:
            raise ValueError("API key is missing")

        self.model_name = model_name
        self.base_url = model_info['base_url']
        self.api_key = model_info['api_key']

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        """
        if model_name == 'gpt-4o':
            return {
                'base_url': os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
                'api_key': os.environ.get('OPENAI_API_KEY', '')
            }
        elif model_name == 'deepseek-chat':
            return {
                'base_url': os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),
                'api_key': os.environ.get('DEEPSEEK_API_KEY', '')
            }
        else:
            return {
                'base_url': os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
                'api_key': os.environ.get('OPENAI_API_KEY', '')
            }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return cls.SUPPORTED_MODELS
