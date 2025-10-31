
import logging
import os


class Config:
    '''Configuration class for Gemini Scan.'''

    def __init__(self, logger: logging.Logger, mcp_port: int = 8765, model: str = 'gemini/gemini-2.5-flash', output_dir: str = '', temperature: float = 0, max_iterations: int = 50, host: str = 'localhost', prompt: str | None = None, confidence: int = 7, project_path: str = ''):
        '''
        Initialize configuration.
        Args:
            logger: The logger instance to use under this config
            model: Name of the model to use (e.g., "gemini/gemini-2.5-flash", "openai/gpt-4")
            output_dir: Directory to store scan outputs
            logger: Logger instance
            max_iterations: Maximum number of tool calling iterations
            project_path: Path to the project being scanned (set during scan)
            temperature: Temperature for model generation
            confidence: Minimum confidence threshold (1-10) for filtering findings
        '''
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
        '''Extract the provider from the model name.'''
        if '/' in model:
            return model.split('/')[0]
        return ''

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        return f"{provider.upper()}_API_KEY"

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        '''Get the API key for a given model from environment variables.'''
        provider = self._get_provider_from_model(model_name)
        if not provider:
            return None
        env_var = self._get_env_var_for_provider(provider)
        return os.getenv(env_var)
