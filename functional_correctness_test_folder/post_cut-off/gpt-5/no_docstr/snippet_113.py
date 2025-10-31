from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict
import os
import math
import pathlib


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
    # Core runtime options
    llm: str = field(default="gpt-4o-mini")
    timeout_seconds: int = field(default=600)
    path: str = field(default="./data")
    temperature: float = field(default=0.2)
    max_tokens: Optional[int] = field(default=None)
    request_retries: int = field(default=2)
    request_retry_backoff_seconds: float = field(default=1.5)

    # API keys (read from env if not provided)
    openai_api_key: Optional[str] = field(default=None, repr=False)
    anthropic_api_key: Optional[str] = field(default=None, repr=False)
    azure_openai_api_key: Optional[str] = field(default=None, repr=False)

    # Optional provider-specific settings
    openai_base_url: Optional[str] = field(default=None)
    azure_openai_endpoint: Optional[str] = field(default=None)
    azure_openai_deployment: Optional[str] = field(default=None)

    def __post_init__(self):
        # Allow environment variable overrides for common settings
        self.llm = os.getenv("BIOMNI_LLM", self.llm)
        self.path = os.getenv("BIOMNI_PATH", self.path)

        # Timeout can come from env; coerce to int if present
        env_timeout = os.getenv("BIOMNI_TIMEOUT_SECONDS")
        if env_timeout is not None:
            try:
                self.timeout_seconds = int(env_timeout)
            except ValueError:
                pass

        # Temperature env override
        env_temp = os.getenv("BIOMNI_TEMPERATURE")
        if env_temp is not None:
            try:
                self.temperature = float(env_temp)
            except ValueError:
                pass

        # Max tokens env override
        env_max_tokens = os.getenv("BIOMNI_MAX_TOKENS")
        if env_max_tokens is not None:
            try:
                self.max_tokens = int(env_max_tokens)
            except ValueError:
                pass

        # Retries
        env_retries = os.getenv("BIOMNI_REQUEST_RETRIES")
        if env_retries is not None:
            try:
                self.request_retries = int(env_retries)
            except ValueError:
                pass

        env_backoff = os.getenv("BIOMNI_REQUEST_RETRY_BACKOFF_SECONDS")
        if env_backoff is not None:
            try:
                self.request_retry_backoff_seconds = float(env_backoff)
            except ValueError:
                pass

        # Provider-specific endpoints
        self.openai_base_url = os.getenv(
            "OPENAI_BASE_URL", self.openai_base_url)
        self.azure_openai_endpoint = os.getenv(
            "AZURE_OPENAI_ENDPOINT", self.azure_openai_endpoint)
        self.azure_openai_deployment = os.getenv(
            "AZURE_OPENAI_DEPLOYMENT", self.azure_openai_deployment)

        # API keys from environment if not supplied explicitly
        if not self.openai_api_key:
            self.openai_api_key = os.getenv(
                "OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        if not self.anthropic_api_key:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.azure_openai_api_key:
            self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")

        # Normalize and ensure path exists
        self.path = str(pathlib.Path(self.path).expanduser().resolve())
        try:
            pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        except Exception:
            # Do not raise during config init
            pass

        # Basic validations and clamping
        if not isinstance(self.llm, str) or not self.llm:
            self.llm = "gpt-4o-mini"

        if not isinstance(self.timeout_seconds, int) or self.timeout_seconds <= 0:
            self.timeout_seconds = 600

        if not isinstance(self.request_retries, int) or self.request_retries < 0:
            self.request_retries = 2

        try:
            self.temperature = float(self.temperature)
        except Exception:
            self.temperature = 0.2
        self.temperature = max(0.0, min(2.0, self.temperature))

        if self.max_tokens is not None:
            try:
                mt = int(self.max_tokens)
                self.max_tokens = mt if mt > 0 else None
            except Exception:
                self.max_tokens = None

        try:
            self.request_retry_backoff_seconds = float(
                self.request_retry_backoff_seconds)
            if not math.isfinite(self.request_retry_backoff_seconds) or self.request_retry_backoff_seconds <= 0:
                self.request_retry_backoff_seconds = 1.5
        except Exception:
            self.request_retry_backoff_seconds = 1.5

    def to_dict(self) -> dict:
        data: Dict[str, Any] = asdict(self)

        # Mask API keys
        def mask(value: Optional[str]) -> Optional[str]:
            if not value:
                return value
            if len(value) <= 8:
                return "****"
            return value[:4] + "****" + value[-4:]

        for key in list(data.keys()):
            if key.endswith("_api_key"):
                data[key] = mask(data[key])

        return {k: v for k, v in data.items() if v is not None}
