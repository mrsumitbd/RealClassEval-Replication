
from dataclasses import dataclass, asdict
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
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"
    api_key: str = os.getenv("BIOMNI_API_KEY", "")

    def __post_init__(self):
        if not self.api_key:
            raise ValueError(
                "API key must be set via environment variable BIOMNI_API_KEY")

    def to_dict(self) -> dict:
        return asdict(self)
