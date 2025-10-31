
import os
from dataclasses import dataclass, field, asdict


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

    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"
    log_level: str = "INFO"
    max_retries: int = 3
    api_key: str = field(default=None, repr=False)
    endpoint: str = "https://api.biomni.com"
    use_cache: bool = True

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        if self.api_key is None:
            self.api_key = os.environ.get("BIOMNI_API_KEY")
        # Allow environment variable overrides for other fields if desired
        self.llm = os.environ.get("BIOMNI_LLM", self.llm)
        self.timeout_seconds = int(os.environ.get(
            "BIOMNI_TIMEOUT_SECONDS", self.timeout_seconds))
        self.path = os.environ.get("BIOMNI_PATH", self.path)
        self.log_level = os.environ.get("BIOMNI_LOG_LEVEL", self.log_level)
        self.max_retries = int(os.environ.get(
            "BIOMNI_MAX_RETRIES", self.max_retries))
        self.endpoint = os.environ.get("BIOMNI_ENDPOINT", self.endpoint)
        use_cache_env = os.environ.get("BIOMNI_USE_CACHE")
        if use_cache_env is not None:
            self.use_cache = use_cache_env.lower() in ("1", "true", "yes")

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
