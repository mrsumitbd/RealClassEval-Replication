
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class BiomniConfig:
    """
    Central configuration for Biomni agent.
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

    # Core settings
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"
    api_key: Optional[str] = None

    # Optional advanced settings
    temperature: float = 0.7
    max_tokens: int = 1500
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        env_map = {
            "BIOMNI_LLM": "llm",
            "BIOMNI_TIMEOUT_SECONDS": "timeout_seconds",
            "BIOMNI_PATH": "path",
            "BIOMNI_API_KEY": "api_key",
            "BIOMNI_TEMPERATURE": "temperature",
            "BIOMNI_MAX_TOKENS": "max_tokens",
            "BIOMNI_TOP_P": "top_p",
            "BIOMNI_FREQUENCY_PENALTY": "frequency_penalty",
            "BIOMNI_PRESENCE_PENALTY": "presence_penalty",
        }

        for env_var, attr in env_map.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert to the correct type based on the attribute's type
                current_type = type(getattr(self, attr))
                try:
                    if current_type is int:
                        cast_value = int(value)
                    elif current_type is float:
                        cast_value = float(value)
                    elif current_type is bool:
                        cast_value = value.lower() in ("1", "true", "yes", "on")
                    else:
                        cast_value = value
                except ValueError:
                    # If conversion fails, skip the override
                    continue
                setattr(self, attr, cast_value)

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return asdict(self)
