
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

        return model.split('/')[0]

    def _get_env_var_for_provider(self, provider: str) -> str:

        return f"{provider.upper()}_API_KEY"

    def _get_api_key_for_model(self, model_name: str) -> str | None:

        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        return os.getenv(env_var)
