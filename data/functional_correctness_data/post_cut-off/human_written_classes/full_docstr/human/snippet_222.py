import os
from typing import Dict, List

class ModelConfig:
    """
    Configuration container for a specific model.
    It loads the necessary API key and base URL from environment variables.
    """
    MODEL_CONFIGS = {'gpt-4o': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-4o'}, 'gpt-4.1': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-4.1'}, 'gpt-4.1-mini': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-4.1-mini'}, 'gpt-4.1-nano': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-4.1-nano'}, 'gpt-5': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-5'}, 'gpt-5-mini': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-5-mini'}, 'gpt-5-nano': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/gpt-5-nano'}, 'o3': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/o3'}, 'o4-mini': {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': 'openai/o4-mini'}, 'gpt-oss-120b': {'provider': 'openai', 'api_key_var': 'OPENROUTER_API_KEY', 'litellm_input_model_name': 'openrouter/openai/gpt-oss-120b'}, 'deepseek-chat': {'provider': 'deepseek', 'api_key_var': 'DEEPSEEK_API_KEY', 'litellm_input_model_name': 'deepseek/deepseek-chat'}, 'deepseek-reasoner': {'provider': 'deepseek', 'api_key_var': 'DEEPSEEK_API_KEY', 'litellm_input_model_name': 'deepseek/deepseek-reasoner'}, 'claude-3.7-sonnet': {'provider': 'anthropic', 'api_key_var': 'ANTHROPIC_API_KEY', 'litellm_input_model_name': 'anthropic/claude-3-7-sonnet-20250219'}, 'claude-sonnet-4': {'provider': 'anthropic', 'api_key_var': 'ANTHROPIC_API_KEY', 'litellm_input_model_name': 'anthropic/claude-sonnet-4-20250514'}, 'claude-opus-4': {'provider': 'anthropic', 'api_key_var': 'ANTHROPIC_API_KEY', 'litellm_input_model_name': 'anthropic/claude-opus-4-20250514'}, 'claude-opus-4.1': {'provider': 'anthropic', 'api_key_var': 'ANTHROPIC_API_KEY', 'litellm_input_model_name': 'anthropic/claude-opus-4-1-20250805'}, 'gemini-2.5-pro': {'provider': 'google', 'api_key_var': 'GEMINI_API_KEY', 'litellm_input_model_name': 'gemini/gemini-2.5-pro'}, 'gemini-2.5-flash': {'provider': 'google', 'api_key_var': 'GEMINI_API_KEY', 'litellm_input_model_name': 'gemini/gemini-2.5-flash'}, 'k2': {'provider': 'moonshot', 'api_key_var': 'MOONSHOT_API_KEY', 'litellm_input_model_name': 'moonshot/kimi-k2-0711-preview'}, 'k2-turbo': {'provider': 'moonshot', 'api_key_var': 'MOONSHOT_API_KEY', 'litellm_input_model_name': 'moonshot/kimi-k2-turbo-preview'}, 'grok-4': {'provider': 'xai', 'api_key_var': 'GROK_API_KEY', 'litellm_input_model_name': 'xai/grok-4-0709'}, 'grok-code-fast-1': {'provider': 'xai', 'api_key_var': 'GROK_API_KEY', 'litellm_input_model_name': 'xai/grok-code-fast-1'}, 'qwen-3-coder': {'provider': 'qwen', 'api_key_var': 'OPENROUTER_API_KEY', 'litellm_input_model_name': 'openrouter/qwen/qwen3-coder'}, 'qwen-3-coder-plus': {'provider': 'qwen', 'api_key_var': 'DASHSCOPE_API_KEY', 'litellm_input_model_name': 'dashscope/qwen3-coder-plus'}, 'glm-4.5': {'provider': 'zhipu', 'api_key_var': 'OPENROUTER_API_KEY', 'litellm_input_model_name': 'openrouter/z-ai/glm-4.5'}}

    def __init__(self, model_name: str):
        """
        Initializes the model configuration.

        Args:
            model_name: The name of the model (e.g., 'gpt-4o', 'deepseek-chat').

        Raises:
            ValueError: If the model is not supported or environment variables are missing.
        """
        self.short_model_name = model_name
        model_info = self._get_model_info(model_name)
        if 'base_url_var' in model_info:
            self.base_url = os.getenv(model_info['base_url_var'])
        else:
            self.base_url = None
        self.api_key = os.getenv(model_info['api_key_var'])
        if not self.api_key:
            raise ValueError(f"Missing required environment variable: {model_info['api_key_var']}")
        self.litellm_input_model_name = model_info.get('litellm_input_model_name', model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieves the configuration details for a given model name.
        For unsupported models, defaults to using OPENAI_BASE_URL and OPENAI_API_KEY.
        """
        if model_name not in self.MODEL_CONFIGS:
            logger.warning(f"Model '{model_name}' not in supported list. Using default OpenAI configuration.")
            return {'provider': 'openai', 'api_key_var': 'OPENAI_API_KEY', 'litellm_input_model_name': model_name}
        return self.MODEL_CONFIGS[model_name]

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Returns a list of all supported model names."""
        return list(cls.MODEL_CONFIGS.keys())