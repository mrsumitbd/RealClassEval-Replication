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
        if not isinstance(logger, logging.Logger):
            raise TypeError("logger must be an instance of logging.Logger")
        if not isinstance(max_iterations, int) or max_iterations < 1:
            raise ValueError("max_iterations must be a positive integer")
        if not (1 <= int(confidence) <= 10):
            raise ValueError("confidence must be between 1 and 10")
        if not (0 <= float(temperature) <= 2):
            raise ValueError("temperature must be between 0 and 2")

        self.logger = logger
        self.mcp_port = int(mcp_port)
        self.host = str(host)
        self.model = str(model)
        self.output_dir = str(output_dir)
        self.temperature = float(temperature)
        self.max_iterations = int(max_iterations)
        self.prompt = prompt
        self.confidence = int(confidence)
        self.project_path = str(project_path)

        self.provider = self._get_provider_from_model(self.model)
        self.api_key_env = self._get_env_var_for_provider(self.provider)
        self.api_key = self._get_api_key_for_model(self.model)

        if self.api_key is None:
            self.logger.debug(
                f"No API key found in environment for provider '{self.provider}' (expected env var: {self.api_key_env})")

    def _get_provider_from_model(self, model: str) -> str:
        '''Extract the provider from the model name.'''
        if not model:
            return ''
        raw = str(model).strip().lower()
        # Accept formats like "provider/model", "provider:model", or just "provider"
        for sep in ('/', ':'):
            if sep in raw:
                return raw.split(sep, 1)[0]
        return raw

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        if not provider:
            return 'API_KEY'
        mapping = {
            'gemini': 'GEMINI_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'groq': 'GROQ_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
            'ai21': 'AI21_API_KEY',
            'perplexity': 'PPLX_API_KEY',
            'azureopenai': 'AZURE_OPENAI_API_KEY',
            'azure-openai': 'AZURE_OPENAI_API_KEY',
            'vertex': 'GOOGLE_APPLICATION_CREDENTIALS',
        }
        return mapping.get(provider.lower(), f'{provider.upper()}_API_KEY')

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        '''Get the API key for a given model from environment variables.'''
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        return os.environ.get(env_var)
