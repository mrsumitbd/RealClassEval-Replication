
from __future__ import annotations

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

    # Core agent settings
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"

    # Optional OpenAI configuration
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1500

    # Additional optional settings
    verbose: bool = False
    retry_attempts: int = 3

    def __post_init__(self) -> None:
        """
        Populate missing API credentials from environment variables.
        """
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_base is None:
            self.api_base = os.getenv("OPENAI_API_BASE")

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the configuration.
        """
        return asdict(self)
