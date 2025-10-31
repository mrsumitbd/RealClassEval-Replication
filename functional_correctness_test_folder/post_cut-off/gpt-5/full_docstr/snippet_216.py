import logging
import os
from typing import Optional


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
        self.mcp_port = int(mcp_port)
        self.model = model.strip()
        self.output_dir = output_dir
        self.temperature = float(temperature)
        self.max_iterations = int(max_iterations)
        self.host = host
        self.prompt = prompt
        self.confidence = int(confidence)
        self.project_path = project_path

        if self.confidence < 1 or self.confidence > 10:
            raise ValueError('confidence must be between 1 and 10')
        if self.max_iterations < 1:
            raise ValueError('max_iterations must be >= 1')
        if self.temperature < 0:
            raise ValueError('temperature must be >= 0')

        self.provider = self._get_provider_from_model(self.model)
        self.api_key_env_var = self._get_env_var_for_provider(self.provider)
        self.api_key = self._get_api_key_for_model(self.model)

    def _get_provider_from_model(self, model: str) -> str:
        '''Extract the provider from the model name.'''
        if not model or not isinstance(model, str):
            return 'unknown'
        # Expected format "provider/model-name"
        parts = model.split('/', 1)
        provider = parts[0].strip().lower() if parts else 'unknown'
        return provider or 'unknown'

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        if not provider:
            return 'API_KEY'
        provider = provider.lower()

        mapping_primary = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'groq': 'GROQ_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'azure': 'AZURE_OPENAI_API_KEY',
            'azure-openai': 'AZURE_OPENAI_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'gcp': 'GOOGLE_API_KEY',
            'vertex': 'GOOGLE_API_KEY',
            'gemini': 'GEMINI_API_KEY',
            'perplexity': 'PERPLEXITY_API_KEY',
            'huggingface': 'HUGGINGFACE_API_KEY',
            'hf': 'HUGGINGFACE_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
            'xai': 'XAI_API_KEY',
            'ollama': '',  # typically no API key required
        }

        env_var = mapping_primary.get(provider)
        if env_var is None:
            # Fallback to conventional pattern
            env_var = f'{provider.upper()}_API_KEY'

        return env_var

    def _get_api_key_for_model(self, model_name: str) -> Optional[str]:
        '''Get the API key for a given model from environment variables.'''
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)

        if provider == 'ollama':
            return None

        # For Gemini, try both GEMINI_API_KEY and GOOGLE_API_KEY commonly used
        if provider == 'gemini':
            return os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

        # For Google-related providers, also try GEMINI_API_KEY as fallback
        if provider in ('google', 'gcp', 'vertex'):
            return os.getenv(env_var) or os.getenv('GEMINI_API_KEY')

        return os.getenv(env_var) if env_var else None
