
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
        if os.getenv('BIOMNI_LLM'):
            self.llm = os.getenv('BIOMNI_LLM')
        if os.getenv('BIOMNI_TIMEOUT_SECONDS'):
            self.timeout_seconds = int(os.getenv('BIOMNI_TIMEOUT_SECONDS'))
        if os.getenv('BIOMNI_PATH'):
            self.path = os.getenv('BIOMNI_PATH')

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
