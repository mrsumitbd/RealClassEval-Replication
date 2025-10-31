
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
        if 'gemini' in model:
            return 'gemini_provider'
        elif 'openai' in model:
            return 'openai_provider'
        else:
            return 'default_provider'

    def _get_env_var_for_provider(self, provider: str) -> str:
        if provider == 'gemini_provider':
            return 'GEMINI_API_KEY'
        elif provider == 'openai_provider':
            return 'OPENAI_API_KEY'
        else:
            return 'DEFAULT_API_KEY'

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        api_key = os.getenv(env_var)
        if not api_key:
            self.logger.warning(
                f"No API key found for {provider} in environment variable {env_var}")
        return api_key
