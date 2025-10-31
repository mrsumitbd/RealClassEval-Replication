from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import os


@dataclass
class BiomniConfig:
    '''Central configuration for Biomni agent.
    All settings are optional and have sensible defaults.
    API keys are still read from environment variables to maintain
    compatibility with existing .env file structure.
    Usage:
        # Create config with defaults
        config = BiomniConfig()
        # Override specific settings
        config = BiomniConfig(llm="gpt-4", timeout_seconds=1200)
        # Modify after creation
        config.path = "./custom_data"
    '''

    # Core settings
    llm: str = "gpt-4"
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    timeout_seconds: int = 600
    path: str = "./data"
    log_level: str = "INFO"
    retries: int = 3

    # Network
    api_base: Optional[str] = None
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None

    # API keys (read from environment if present)
    openai_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Freeform extras
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        # Compatibility with common .env structures
        self.openai_api_key = self._env_str(
            "OPENAI_API_KEY", self.openai_api_key)
        self.azure_openai_api_key = self._env_str(
            "AZURE_OPENAI_API_KEY", self.azure_openai_api_key)
        self.azure_openai_endpoint = self._env_str(
            "AZURE_OPENAI_ENDPOINT", self.azure_openai_endpoint)
        self.azure_openai_deployment = self._env_str(
            "AZURE_OPENAI_DEPLOYMENT", self.azure_openai_deployment)
        self.anthropic_api_key = self._env_str(
            "ANTHROPIC_API_KEY", self.anthropic_api_key)
        self.google_api_key = self._env_str(
            "GOOGLE_API_KEY", self.google_api_key)

        self.api_base = self._env_str("API_BASE", self.api_base)
        self.http_proxy = self._env_str("HTTP_PROXY", self.http_proxy)
        self.https_proxy = self._env_str("HTTPS_PROXY", self.https_proxy)

        # Optional overrides for core config
        self.llm = self._env_str("BIOMNI_LLM", self.llm)
        self.temperature = self._env_float("LLM_TEMPERATURE", self.temperature)
        self.max_tokens = self._env_int("MAX_TOKENS", self.max_tokens)
        self.timeout_seconds = self._env_int(
            "BIOMNI_TIMEOUT", self.timeout_seconds)
        self.path = self._env_str("BIOMNI_PATH", self.path)
        self.log_level = self._env_str("LOG_LEVEL", self.log_level)
        self.retries = self._env_int("RETRIES", self.retries)

        # Load BIOMNI_EXTRA_* into extra dict
        prefix = "BIOMNI_EXTRA_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                self.extra[key[len(prefix):].lower()] = value

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)

    @staticmethod
    def _env_str(name: str, default: Optional[str]) -> Optional[str]:
        val = os.getenv(name)
        return val if val is not None and val != "" else default

    @staticmethod
    def _env_int(name: str, default: Optional[int]) -> Optional[int]:
        val = os.getenv(name)
        if val is None or val.strip() == "":
            return default
        try:
            return int(val)
        except ValueError:
            return default

    @staticmethod
    def _env_float(name: str, default: Optional[float]) -> Optional[float]:
        val = os.getenv(name)
        if val is None or val.strip() == "":
            return default
        try:
            return float(val)
        except ValueError:
            return default
