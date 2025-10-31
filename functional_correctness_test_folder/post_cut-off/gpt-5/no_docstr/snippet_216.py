import logging
import os
from pathlib import Path
from typing import Optional


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
        prompt: Optional[str] = None,
        confidence: int = 7,
        project_path: str = '',
    ):
        self.logger = logger
        self.mcp_port = int(mcp_port)
        self.model = str(model).strip()
        self.temperature = float(temperature)
        self.max_iterations = int(max_iterations)
        self.host = str(host).strip()
        self.prompt = '' if prompt is None else str(prompt)
        self.confidence = int(confidence)
        self.project_path = str(project_path).strip()

        if self.confidence < 0:
            self.confidence = 0
        if self.confidence > 10:
            self.confidence = 10

        self.provider = self._get_provider_from_model(self.model)
        self.env_var_for_provider = self._get_env_var_for_provider(
            self.provider)
        self.api_key = self._get_api_key_for_model(self.model)

        self.output_dir = str(output_dir).strip()
        if self.output_dir:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        if self.project_path:
            Path(self.project_path).mkdir(parents=True, exist_ok=True)

        if hasattr(self.logger, "debug"):
            self.logger.debug(
                f"Config initialized: provider={self.provider}, model={self.model}, "
                f"env_var={self.env_var_for_provider}, api_key_present={bool(self.api_key)}, "
                f"output_dir={self.output_dir or '(none)'}, "
                f"project_path={self.project_path or '(none)'}"
            )

    def _get_provider_from_model(self, model: str) -> str:
        if not model:
            return ''
        parts = str(model).strip().split('/', 1)
        return parts[0].lower().strip() if parts else ''

    def _get_env_var_for_provider(self, provider: str) -> str:
        mapping = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'gemini': 'GOOGLE_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'googleai': 'GOOGLE_API_KEY',
            'groq': 'GROQ_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'cohere': 'COHERE_API_KEY',
            'perplexity': 'PERPLEXITY_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'replicate': 'REPLICATE_API_TOKEN',
            'ai21': 'AI21_API_KEY',
            'nvidia': 'NVIDIA_API_KEY',
            'bedrock': 'AWS_BEDROCK_API_KEY',
        }
        key = mapping.get(provider.lower().strip()) if provider else None
        return key or ''

    def _get_api_key_for_model(self, model_name: str) -> str | None:
        provider = self._get_provider_from_model(model_name)
        env_var = self._get_env_var_for_provider(provider)
        if not env_var:
            return None
        return os.environ.get(env_var) or None
