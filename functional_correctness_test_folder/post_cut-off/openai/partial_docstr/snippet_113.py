
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
    max_tokens: int = 1024
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

        for env_var, field_name in env_map.items():
            value = os.getenv(env_var)
            if value is None:
                continue

            # Convert to the appropriate type
            if field_name in {"timeout_seconds", "max_tokens"}:
                try:
                    value = int(value)
                except ValueError:
                    continue
            elif field_name in {"temperature", "top_p", "frequency_penalty", "presence_penalty"}:
                try:
                    value = float(value)
                except ValueError:
                    continue

            setattr(self, field_name, value)

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return asdict(self)
