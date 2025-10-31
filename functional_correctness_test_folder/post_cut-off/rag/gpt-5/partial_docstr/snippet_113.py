from dataclasses import dataclass, asdict
from typing import Optional, Any
import os


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {'1', 'true', 'yes', 'y', 'on'}


@dataclass
class BiomniConfig:
    """Central configuration for Biomni agent.
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
    """

    # General settings
    path: str = "./data"
    llm: str = "gpt-4o-mini"
    timeout_seconds: int = 600
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    retries: int = 3
    log_level: str = "INFO"
    verify_ssl: bool = True
    proxy: Optional[str] = None
    user_agent: str = "biomni-agent/1.0"

    # API keys and provider settings (read from environment, if present)
    openai_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    biomni_api_key: Optional[str] = None

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        # String values
        env_str_overrides = [
            ('BIOMNI_LLM', 'llm'),
            ('BIOMNI_PATH', 'path'),
            ('BIOMNI_DATA_PATH', 'path'),  # preferred, if present
            ('BIOMNI_LOG_LEVEL', 'log_level'),
            ('OPENAI_API_KEY', 'openai_api_key'),
            ('AZURE_OPENAI_API_KEY', 'azure_openai_api_key'),
            ('AZURE_OPENAI_ENDPOINT', 'azure_openai_endpoint'),
            ('OPENAI_API_BASE', 'azure_openai_endpoint'),  # common alt var
            ('ANTHROPIC_API_KEY', 'anthropic_api_key'),
            ('GOOGLE_API_KEY', 'google_api_key'),
            ('BIOMNI_API_KEY', 'biomni_api_key'),
            ('BIOMNI_USER_AGENT', 'user_agent'),
        ]
        for env_name, attr in env_str_overrides:
            val = os.getenv(env_name)
            if val:
                setattr(self, attr, val)

        # Fall back to generic LOG_LEVEL if BIOMNI_LOG_LEVEL not set
        if os.getenv('LOG_LEVEL') and not os.getenv('BIOMNI_LOG_LEVEL'):
            self.log_level = os.getenv('LOG_LEVEL', self.log_level)

        # Numeric values
        int_overrides = [
            ('BIOMNI_TIMEOUT_SECONDS', 'timeout_seconds'),
            ('BIOMNI_MAX_TOKENS', 'max_tokens'),
            ('BIOMNI_RETRIES', 'retries'),
        ]
        for env_name, attr in int_overrides:
            val = os.getenv(env_name)
            if val is not None:
                try:
                    setattr(self, attr, int(val))
                except ValueError:
                    pass

        float_overrides = [
            ('BIOMNI_TEMPERATURE', 'temperature'),
        ]
        for env_name, attr in float_overrides:
            val = os.getenv(env_name)
            if val is not None:
                try:
                    setattr(self, attr, float(val))
                except ValueError:
                    pass

        # Boolean values
        bool_overrides = [
            ('BIOMNI_VERIFY_SSL', 'verify_ssl'),
        ]
        for env_name, attr in bool_overrides:
            val = os.getenv(env_name)
            if val is not None:
                try:
                    setattr(self, attr, _parse_bool(val))
                except Exception:
                    pass

        # Proxy (prefer HTTPS over HTTP if both set)
        https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
        http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
        if https_proxy:
            self.proxy = https_proxy
        elif http_proxy and not self.proxy:
            self.proxy = http_proxy

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return asdict(self)
