
from dataclasses import dataclass, asdict
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
    llm: Optional[str] = "gpt-3.5-turbo"
    timeout_seconds: Optional[int] = 600
    path: Optional[str] = "./data"
    max_retries: Optional[int] = 3
    verbose: Optional[bool] = False

    def __post_init__(self):
        pass

    def to_dict(self) -> dict:
        return asdict(self)
