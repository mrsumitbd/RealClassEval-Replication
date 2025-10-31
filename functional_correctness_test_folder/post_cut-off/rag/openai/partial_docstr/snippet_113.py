
from __future__ import annotations

import os
from dataclasses import dataclass, field, fields, asdict
from typing import Any, Optional

try:
    # Python 3.10+ has a dedicated bool parser in the standard library
    from distutils.util import strtobool  # type: ignore
except Exception:
    # Fallback if distutils is not available
    def strtobool(val: str) -> bool:  # pragma: no cover
        return val.lower() in ("1", "true", "yes", "on")


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
    """Name of the LLM model to use."""

    timeout_seconds: int = 600
    """Maximum number of seconds to wait for a response."""

    path: str = "./data"
    """Base directory for storing agent data."""

    api_key: Optional[str] = None
    """API key for external services.  Loaded from BIOMNI_API_KEY if set."""

    # Optional flags
    verbose: bool = False
    """Enable verbose logging."""

    def __post_init__(self) -> None:
        """Load any environment variable overrides if they exist."""
        for f in fields(self):
            env_name = f"BIOMNI_{f.name.upper()}"
            if env_name in os.environ:
                raw_val = os.environ[env_name]
                # Determine the type of the field and cast accordingly
                if f.type is bool or f.type is Optional[bool]:
                    try:
                        cast_val = bool(strtobool(raw_val))
                    except ValueError:
                        cast_val = raw_val.lower() in ("1", "true", "yes", "on")
                elif f.type is int or f.type is Optional[int]:
                    try:
                        cast_val = int(raw_val)
                    except ValueError:
                        cast_val = f.default
                elif f.type is float or f.type is Optional[float]:
                    try:
                        cast_val = float(raw_val)
                    except ValueError:
                        cast_val = f.default
                else:
                    cast_val = raw_val
                setattr(self, f.name, cast_val)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for easy access."""
        return asdict(self)
