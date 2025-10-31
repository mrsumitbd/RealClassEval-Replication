
import logging
import os


class Config:

    def __init__(self, logger: logging.Logger, mcp_port: int = 8765, model: str = 'gemini/gemini-2.5-flash', output_dir: str = '', temperature: float = 0, max_iterations: int = 50, host: str = 'localhost', prompt: str | None = None, confidence: int = 7, project_path: str = ''):
        self.logger = logger
        self.mcp_port = mcp_port
        self.model = model
        self.output_dir = output_dir
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.host = host
        self.prompt = prompt
        self.confidence = confidence
        self.project_path = project_path

    def _get_provider_from_model(self, model: str) -> str:
        provider_map = {
            'gemini': 'google',
            'gpt': 'openai',
            'claude': 'anthropic',
            'command': 'cohere',
            'mistral': 'mistral',
            'llama': 'meta'
        }
        for key in provider_map:
            if key in model.lower():
                return provider_map[key]
        self.logger.warning(
            f"Unknown model: {model}. Unable to determine provider.")
        return ''

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        env_var_map = {
            'google': 'GOOGLE_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'meta': 'META_API_KEY'
        }
        return env_var_map.get(provider, '')

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        provider = self._get_provider_from_model(model_name)
        if not provider:
            return None
        env_var = self._get_env_var_for_provider(provider)
        if not env_var:
            self.logger.warning(
                f"Unknown provider: {provider}. Unable to retrieve API key.")
            return None
        return os.getenv(env_var)
