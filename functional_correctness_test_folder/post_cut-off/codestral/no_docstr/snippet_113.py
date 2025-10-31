
from dataclasses import dataclass, asdict


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
    max_tokens: int = 1000
    temperature: float = 0.7

    def __post_init__(self):
        self.api_key = os.getenv("API_KEY")

    def to_dict(self) -> dict:
        return asdict(self)
