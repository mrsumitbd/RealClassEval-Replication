
from dataclasses import dataclass, asdict, fields
import os


@dataclass
class BiomniConfig:
    """Central configuration for Biomni agent.

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
    """
    # Add default fields here, for example:
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        for field in fields(self):
            env_var = f"BIOMNI_{field.name.upper()}"
            if env_var in os.environ:
                setattr(self, field.name, type(
                    getattr(self, field.name))(os.environ[env_var]))

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return asdict(self)
