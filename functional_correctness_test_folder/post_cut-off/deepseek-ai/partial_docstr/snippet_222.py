
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.base_url, self.api_key = self._get_model_info(model_name).values()

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        supported_models = self.get_supported_models()
        if model_name in supported_models:
            prefix = model_name.upper().replace('-', '_')
            base_url = os.getenv(f"{prefix}_BASE_URL")
            api_key = os.getenv(f"{prefix}_API_KEY")
        else:
            base_url = os.getenv("OPENAI_BASE_URL")
            api_key = os.getenv("OPENAI_API_KEY")
        return {"base_url": base_url, "api_key": api_key}

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return [
            "gpt-4",
            "gpt-3.5-turbo",
            "claude-2",
            "llama-2-70b"
        ]
