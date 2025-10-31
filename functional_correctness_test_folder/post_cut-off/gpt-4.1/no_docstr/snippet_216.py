
import logging
import os


class Config:

    def __init__(
        self,
        logger: logging.Logger,
        mcp_port: int = 8765,
        model: str = 'gemini/gemini-2.5-flash',
        output_dir: str = '',
        temperature: float = 0,
        max_iterations: int = 50,
        host: str = 'localhost',
        prompt: str | None = None,
        confidence: int = 7,
        project_path: str = ''
    ):
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
        model = model.lower()
        if model.startswith('gemini/'):
            return 'gemini'
        elif model.startswith('openai/'):
            return 'openai'
        elif model.startswith('anthropic/'):
            return 'anthropic'
        elif model.startswith('mistral/'):
            return 'mistral'
        else:
            return 'unknown'

    def _get_env_var_for_provider(self, provider: str) -> str:
        provider = provider.lower()
        if provider == 'gemini':
            return 'GEMINI_API_KEY'
        elif provider == 'openai':
            return 'OPENAI_API_KEY'
        elif provider == 'anthropic':
            return 'ANTHROPIC_API_KEY'
        elif provider == 'mistral':
            return 'MISTRAL_API_KEY'
        else:
            return ''

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        if env_var:
            return os.environ.get(env_var)
        return None
