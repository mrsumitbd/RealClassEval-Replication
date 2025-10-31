
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
    max_retries: int = 3
    api_key: str = None
    api_base: str = None

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        self.api_key = os.getenv("BIOMNI_API_KEY", self.api_key)
        self.api_base = os.getenv("BIOMNI_API_BASE", self.api_base)

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
