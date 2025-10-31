
import os
from typing import Dict, List


class ModelConfig:
    '''
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    '''
    SUPPORTED_MODELS = [
        'model1', 'model2']  # Replace with actual supported model names

    def __init__(self, model_name: str):
        model_info = self._get_model_info(model_name)
        self.model_name = model_name
        self.base_url = model_info['base_url']
        self.api_key = model_info['api_key']

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        '''
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        '''
        if model_name in self.SUPPORTED_MODELS:
            base_url_env_var = f'{model_name.upper()}_BASE_URL'
            api_key_env_var = f'{model_name.upper()}_API_KEY'
            return {
                'base_url': os.environ.get(base_url_env_var),
                'api_key': os.environ.get(api_key_env_var)
            }
        else:
            return {
                'base_url': os.environ.get('OPENAI_BASE_URL'),
                'api_key': os.environ.get('OPENAI_API_KEY')
            }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        '''Returns a list of all supported model names.'''
        return cls.SUPPORTED_MODELS
