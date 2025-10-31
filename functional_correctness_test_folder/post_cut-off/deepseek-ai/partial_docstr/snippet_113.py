
from dataclasses import dataclass, asdict
import os
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
    llm: Optional[str] = None
    timeout_seconds: Optional[int] = None
    path: Optional[str] = None

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        if self.llm is None and "BIOMNI_LLM" in os.environ:
            self.llm = os.environ["BIOMNI_LLM"]
        if self.timeout_seconds is None and "BIOMNI_TIMEOUT_SECONDS" in os.environ:
            self.timeout_seconds = int(os.environ["BIOMNI_TIMEOUT_SECONDS"])
        if self.path is None and "BIOMNI_PATH" in os.environ:
            self.path = os.environ["BIOMNI_PATH"]

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
