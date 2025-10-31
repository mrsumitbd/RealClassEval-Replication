import logging
import os
from typing import Optional


class Config:
    def __init__(self, logger: logging.Logger, mcp_port: int = 8765, model: str = 'gemini/gemini-2.5-flash', output_dir: str = '', temperature: float = 0, max_iterations: int = 50, host: str = 'localhost', prompt: str | None = None, confidence: int = 7, project_path: str = ''):
        self.logger = logger
        self.mcp_port = int(mcp_port)
        self.model = model
        self.output_dir = output_dir
        self.temperature = float(temperature)
        self.max_iterations = int(max_iterations)
        self.host = host
        self.prompt = prompt
        self.confidence = int(confidence)
        self.project_path = project_path

        self.provider = self._get_provider_from_model(self.model)
        self.api_key = self._get_api_key_for_model(self.model)

    def _get_provider_from_model(self, model: str) -> str:
        m = (model or '').strip().lower()
        if not m:
            return ''
        if '/' in m:
            return m.split('/', 1)[0]

        # Infer from common model name prefixes
        if m.startswith('gpt') or 'gpt-' in m:
            return 'openai'
        if m.startswith('claude'):
            return 'anthropic'
        if m.startswith('gemini') or 'bison' in m or 'palm' in m:
            return 'gemini'
        if m.startswith('mistral') or m.startswith('mixtral'):
            return 'mistral'
        if m.startswith('groq'):
            return 'groq'
        if m.startswith('cohere') or 'command' in m:
            return 'cohere'
        if m.startswith('openrouter'):
            return 'openrouter'
        if m.startswith('google'):
            return 'google'
        return ''

    def _get_env_var_for_provider(self, provider: str) -> str:
        '''Get the expected environment variable name for a provider.'''
        p = (provider or '').strip().lower()
        mapping = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'groq': 'GROQ_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'gemini': 'GEMINI_API_KEY',
        }
        return mapping.get(p, '')

    def _get_api_key_for_model(self, model_name: str) -> Optional[str]:
        provider = self._get_provider_from_model(model_name)
        primary_env = self._get_env_var_for_provider(provider)

        # Try primary env var
        if primary_env and os.environ.get(primary_env):
            return os.environ.get(primary_env)

        # Fallbacks for Gemini/Google ambiguity
        if provider in ('gemini', 'google'):
            for env_var in ('GEMINI_API_KEY', 'GOOGLE_API_KEY'):
                if os.environ.get(env_var):
                    return os.environ.get(env_var)

        # No key found
        return None
