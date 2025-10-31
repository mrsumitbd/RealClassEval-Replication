from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict
import os


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on", "y", "t"}


def _maybe_int(value: Optional[str], default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _maybe_float(value: Optional[str], default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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
    # General settings
    llm: str = "gpt-4"
    timeout_seconds: int = 600
    path: str = "./data"
    verbose: bool = False
    temperature: float = 0.2
    max_tokens: int = 2048

    # API keys (pulled from environment if present)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Additional optional routing/config
    organization: Optional[str] = None
    project: Optional[str] = None

    # Allow custom env prefix for overrides (defaults to BIOMNI_)
    env_prefix: str = field(default="BIOMNI_", repr=False)

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        # Override core settings from env if present
        env_llm = os.getenv(f"{self.env_prefix}LLM")
        if env_llm:
            self.llm = env_llm

        env_timeout = os.getenv(f"{self.env_prefix}TIMEOUT_SECONDS")
        self.timeout_seconds = _maybe_int(env_timeout, self.timeout_seconds)

        env_path = os.getenv(f"{self.env_prefix}PATH")
        if env_path:
            self.path = env_path

        env_verbose = os.getenv(f"{self.env_prefix}VERBOSE")
        if env_verbose is not None:
            self.verbose = _parse_bool(env_verbose)

        env_temp = os.getenv(f"{self.env_prefix}TEMPERATURE")
        self.temperature = _maybe_float(env_temp, self.temperature)

        env_max_tokens = os.getenv(f"{self.env_prefix}MAX_TOKENS")
        self.max_tokens = _maybe_int(env_max_tokens, self.max_tokens)

        env_org = os.getenv(f"{self.env_prefix}ORGANIZATION")
        if env_org:
            self.organization = env_org

        env_project = os.getenv(f"{self.env_prefix}PROJECT")
        if env_project:
            self.project = env_project

        # API keys: prefer explicitly provided values, otherwise load from env
        self.openai_api_key = self.openai_api_key or os.getenv(
            "OPENAI_API_KEY") or os.getenv(f"{self.env_prefix}OPENAI_API_KEY")
        self.anthropic_api_key = self.anthropic_api_key or os.getenv(
            "ANTHROPIC_API_KEY") or os.getenv(f"{self.env_prefix}ANTHROPIC_API_KEY")
        self.azure_openai_api_key = self.azure_openai_api_key or os.getenv(
            "AZURE_OPENAI_API_KEY") or os.getenv(f"{self.env_prefix}AZURE_OPENAI_API_KEY")
        self.google_api_key = self.google_api_key or os.getenv(
            "GOOGLE_API_KEY") or os.getenv(f"{self.env_prefix}GOOGLE_API_KEY")

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        data: Dict[str, Any] = asdict(self)

        # Mask API keys
        def _mask(v: Optional[str]) -> Optional[str]:
            if not v:
                return v
            if len(v) <= 8:
                return "***"
            return f"{'*' * (len(v) - 4)}{v[-4:]}"  # keep last 4

        for k in list(data.keys()):
            if k.endswith("_api_key"):
                data[k] = _mask(data[k])

        return data
