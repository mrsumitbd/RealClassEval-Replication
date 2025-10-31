import logging
import os


class Config:
    """Configuration class for Gemini Scan."""

    def __init__(self, logger: logging.Logger, mcp_port: int = 8765, model: str = 'gemini/gemini-2.5-flash', output_dir: str = '', temperature: float = 0, max_iterations: int = 50, host: str = 'localhost', prompt: str | None = None, confidence: int = 7, project_path: str = ''):
        """
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
        """
        self.logger = logger

        self.host = host
        self.mcp_port = int(mcp_port)
        self.model = model
        self.prompt = prompt

        self.output_dir = os.path.abspath(
            os.path.expanduser(output_dir)) if output_dir else ''
        self.project_path = os.path.abspath(
            os.path.expanduser(project_path)) if project_path else ''

        self.max_iterations = max(1, int(max_iterations))
        self.temperature = float(max(0.0, min(2.0, float(temperature))))
        self.confidence = max(1, min(10, int(confidence)))

        self.provider = self._get_provider_from_model(self.model)
        self.api_key_env = self._get_env_var_for_provider(self.provider)
        self.api_key = self._get_api_key_for_model(self.model)

    def _get_provider_from_model(self, model: str) -> str:
        """Extract the provider from the model name."""
        if not model:
            return ''
        model_lower = model.strip().lower()
        if '/' in model_lower:
            return model_lower.split('/', 1)[0]

        # Heuristics if provider is omitted
        if 'gemini' in model_lower or model_lower.startswith('google-'):
            return 'gemini'
        if model_lower.startswith('gpt') or 'openai' in model_lower:
            return 'openai'
        if 'claude' in model_lower or 'anthropic' in model_lower:
            return 'anthropic'
        if 'mistral' in model_lower or 'mixtral' in model_lower:
            return 'mistral'
        if 'groq' in model_lower:
            return 'groq'
        if 'llama' in model_lower or 'meta' in model_lower:
            return 'meta'
        if 'cohere' in model_lower:
            return 'cohere'
        if 'azure' in model_lower:
            return 'azure'

        return model_lower

    def _get_env_var_for_provider(self, provider: str) -> str:
        """Get the expected environment variable name for a provider."""
        mapping = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'gemini': 'GEMINI_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'groq': 'GROQ_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'azure': 'AZURE_OPENAI_API_KEY',
            'meta': 'META_API_KEY',
        }
        return mapping.get(provider.lower(), f'{provider.upper()}_API_KEY')

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        """Get the API key for a given model from environment variables."""
        provider = self._get_provider_from_model(model_name)
        primary_env = self._get_env_var_for_provider(provider)
        key = os.environ.get(primary_env)

        if key:
            return key

        # Fallbacks for certain providers
        if provider == 'gemini':
            # Some environments use GOOGLE_API_KEY for Gemini
            key = os.environ.get(
                'GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
            if key:
                return key
        if provider == 'azure':
            # Azure OpenAI may use either AZURE_OPENAI_API_KEY or OPENAI_API_KEY depending on setup
            key = os.environ.get('OPENAI_API_KEY') or os.environ.get(
                'AZURE_OPENAI_API_KEY')
            if key:
                return key

        return None
