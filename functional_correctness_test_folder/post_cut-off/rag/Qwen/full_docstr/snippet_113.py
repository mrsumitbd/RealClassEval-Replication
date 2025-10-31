
from dataclasses import dataclass, field
from typing import Any, Optional
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

    llm: str = field(default="gpt-3.5-turbo")
    timeout_seconds: int = field(default=600)
    path: str = field(default="./data")
    api_key: Optional[str] = field(default=None)

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        self.api_key = self.api_key or os.getenv(
            'BIOMNI_API_KEY', self.api_key)

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return {
            "llm": self.llm,
            "timeout_seconds": self.timeout_seconds,
            "path": self.path,
            "api_key": self.api_key
        }
