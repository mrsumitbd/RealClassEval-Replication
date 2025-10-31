from dataclasses import dataclass, field, asdict
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

    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"
    log_level: str = "INFO"
    api_url: str = "https://api.biomni.com"
    # Add more config fields as needed

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        # For each field, check if an env var exists and override
        for field_ in self.__dataclass_fields__:
            env_var = f"BIOMNI_{field_.upper()}"
            if env_var in os.environ:
                value = os.environ[env_var]
                # Try to cast to the correct type
                field_type = self.__dataclass_fields__[field_].type
                try:
                    if field_type is int:
                        value = int(value)
                    elif field_type is float:
                        value = float(value)
                    # Add more type conversions as needed
                except Exception:
                    pass
                setattr(self, field_, value)

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return asdict(self)
