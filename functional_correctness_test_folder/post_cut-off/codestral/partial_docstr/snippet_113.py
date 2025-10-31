
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
    timeout_seconds: int = 300
    path: str = "./data"
    api_key: str = None

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        if os.getenv("BIO_MNI_LLM") is not None:
            self.llm = os.getenv("BIO_MNI_LLM")
        if os.getenv("BIO_MNI_TIMEOUT_SECONDS") is not None:
            self.timeout_seconds = int(os.getenv("BIO_MNI_TIMEOUT_SECONDS"))
        if os.getenv("BIO_MNI_PATH") is not None:
            self.path = os.getenv("BIO_MNI_PATH")
        if os.getenv("BIO_MNI_API_KEY") is not None:
            self.api_key = os.getenv("BIO_MNI_API_KEY")

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
