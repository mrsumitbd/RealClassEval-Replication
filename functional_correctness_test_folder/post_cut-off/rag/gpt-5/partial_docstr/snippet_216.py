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
        self.host = host
        self.mcp_port = int(mcp_port)
        self.model = model
        self.output_dir = output_dir
        self.temperature = float(temperature)
        self.max_iterations = int(max_iterations)
        self.prompt = prompt
        self.confidence = max(1, min(10, int(confidence)))
        self.project_path = project_path

        self.provider = self._get_provider_from_model(model)
        self.api_key_env_var = self._get_env_var_for_provider(self.provider)
        self.api_key = self._get_api_key_for_model(model)

    def _get_provider_from_model(self, model: str) -> str:
        '''Extract the provider from the model name.'''
        if not model:
            return 'gemini'
        m = model.strip().lower()

        if '/' in m:
            return m.split('/', 1)[0]
        if ':' in m:
            return m.split(':', 1)[0]

        if m.startswith('gemini') or 'google' in m:
            return 'gemini'
        if m.startswith('gpt') or m.startswith('o-') or m.startswith('o3') or 'openai' in m:
            return 'openai'
        if m.startswith('claude') or 'anthropic' in m:
            return 'anthropic'
        if m.startswith('mistral'):
            return 'mistral'
        if m.startswith('command') or 'cohere' in m:
            return 'cohere'
        if 'openrouter' in m:
            return 'openrouter'
        if 'azure' in m and 'openai' in m:
            return 'azure-openai'
        if 'groq' in m:
            return 'groq'
        if 'perplexity' in m or m.startswith('pplx'):
            return 'perplexity'
        if 'deepseek' in m:
            return 'deepseek'
        if 'together' in m:
            return 'together'
        if 'fireworks' in m:
            return 'fireworks'

        return m.split('-', 1)[0] if '-' in m else m

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        mapping = {
            'openai': 'OPENAI_API_KEY',
            'azure-openai': 'AZURE_OPENAI_API_KEY',
            'gemini': 'GOOGLE_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
            'groq': 'GROQ_API_KEY',
            'perplexity': 'PPLX_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'fireworks': 'FIREWORKS_API_KEY',
        }
        return mapping.get(provider, f'{provider.upper()}_API_KEY')

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        '''Get the API key for a given model from environment variables.'''
        provider = self._get_provider_from_model(model_name)

        candidates: list[str] = []
        if provider in ('gemini', 'google'):
            candidates = ['GEMINI_API_KEY', 'GOOGLE_API_KEY']
        elif provider == 'azure-openai':
            candidates = ['AZURE_OPENAI_API_KEY']
        else:
            candidates = [self._get_env_var_for_provider(provider)]

        for var in candidates:
            val = os.getenv(var)
            if val:
                return val
        return None
