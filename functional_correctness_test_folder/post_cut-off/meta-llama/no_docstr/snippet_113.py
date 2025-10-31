
from dataclasses import dataclass, asdict, field
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
    llm: Optional[str] = field(default="gpt-3.5-turbo")
    timeout_seconds: Optional[int] = field(default=300)
    path: Optional[str] = field(default="./data")
    max_retries: Optional[int] = field(default=3)

    def __post_init__(self):
        if self.timeout_seconds <= 0:
            raise ValueError("Timeout must be greater than zero")

    def to_dict(self) -> dict:
        return asdict(self)
