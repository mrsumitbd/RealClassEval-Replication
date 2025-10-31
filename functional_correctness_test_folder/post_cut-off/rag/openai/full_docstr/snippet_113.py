
from __future__ import annotations

import os
from dataclasses import dataclass


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
    api_key: str | None = None

    def __post_init__(self) -> None:
        """Load any environment variable overrides if they exist."""
        env_map = {
            "BIOMNI_LLM": "llm",
            "BIOMNI_TIMEOUT_SECONDS": "timeout_seconds",
            "BIOMNI_PATH": "path",
            "BIOMNI_API_KEY": "api_key",
        }
        for env_var, attr in env_map.items():
            val = os.getenv(env_var)
            if val is not None:
                if attr == "timeout_seconds":
                    try:
                        setattr(self, attr, int(val))
                    except ValueError:
                        # ignore invalid integer values
                        pass
                else:
                    setattr(self, attr, val)

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return {
            "llm": self.llm,
            "timeout_seconds": self.timeout_seconds,
            "path": self.path,
            "api_key": self.api_key,
        }
