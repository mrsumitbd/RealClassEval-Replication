
from dataclasses import dataclass, field, asdict
from typing import Optional


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
    proxy: Optional[str] = None
    use_cache: bool = True

    def __post_init__(self):
        if self.timeout_seconds < 0:
            raise ValueError("timeout_seconds must be non-negative")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("log_level must be a valid logging level")

    def to_dict(self) -> dict:
        return asdict(self)
