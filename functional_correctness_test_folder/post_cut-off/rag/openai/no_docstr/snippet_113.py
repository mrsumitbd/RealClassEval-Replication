
from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from distutils.util import strtobool
from typing import Any, Dict, Optional


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

    # Core configuration options
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"

    # Optional API credentials (read from env by default)
    api_key: Optional[str] = None
    api_secret: Optional[str] = None

    # Miscellaneous flags
    debug: bool = False

    def __post_init__(self) -> None:
        """Load any environment variable overrides if they exist."""
        # Helper to override a field if an env var is set
        def _override(field_name: str, env_var: str, cast: Any = lambda x: x) -> None:
            value = os.getenv(env_var)
            if value is not None:
                try:
                    cast_value = cast(value)
                except Exception:
                    # If casting fails, fall back to the raw string
                    cast_value = value
                setattr(self, field_name, cast_value)

        # Override core fields
        _override("llm", "BIOMNI_LLM")
        _override("timeout_seconds", "BIOMNI_TIMEOUT_SECONDS", int)
        _override("timeout_seconds", "BIOMNI_TIMEOUT", int)  # legacy alias
        _override("path", "BIOMNI_PATH")

        # Override API credentials
        _override("api_key", "BIOMNI_API_KEY")
        _override("api_secret", "BIOMNI_API_SECRET")

        # Override debug flag
        _override("debug", "BIOMNI_DEBUG", lambda v: bool(strtobool(v)))

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for easy access."""
        return asdict(self)
