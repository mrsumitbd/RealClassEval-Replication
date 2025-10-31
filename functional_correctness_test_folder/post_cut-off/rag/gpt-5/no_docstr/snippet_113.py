from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, Optional, get_args, get_origin


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

    # Core settings
    llm: str = "gpt-4o-mini"
    timeout_seconds: int = 600
    path: Path = field(default_factory=lambda: Path("./data"))

    # Tuning/settings
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    log_level: str = "INFO"

    # Optional API keys (loaded from environment by default)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_openai_api_version: Optional[str] = None

    # Network
    proxy: Optional[str] = None
    verify_ssl: bool = True

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        # Normalize path
        if isinstance(self.path, str):
            self.path = Path(self.path)
        self.path = self.path.expanduser()

        # Apply BIOMNI_ overrides for any config field
        for f in fields(self):
            env_name = f"BIOMNI_{f.name.upper()}"
            if env_name in os.environ:
                value = os.environ[env_name]
                setattr(self, f.name, self._cast_env_value(value, f.type))

        # API key compatibility with common env var names
        self.openai_api_key = (
            self.openai_api_key or os.getenv(
                "OPENAI_API_KEY") or os.getenv("OPENAI_KEY")
        )
        self.anthropic_api_key = self.anthropic_api_key or os.getenv(
            "ANTHROPIC_API_KEY")
        self.google_api_key = (
            self.google_api_key
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
        self.azure_openai_api_key = self.azure_openai_api_key or os.getenv(
            "AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = self.azure_openai_endpoint or os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        )
        self.azure_openai_deployment = self.azure_openai_deployment or os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        )
        self.azure_openai_api_version = self.azure_openai_api_version or os.getenv(
            "AZURE_OPENAI_API_VERSION"
        )

        # Allow generic overrides for common settings
        if os.getenv("LLM"):
            self.llm = os.getenv("LLM")  # type: ignore[assignment]
        if os.getenv("TIMEOUT_SECONDS"):
            self.timeout_seconds = int(
                os.getenv("TIMEOUT_SECONDS", str(self.timeout_seconds)))
        if os.getenv("DATA_PATH"):
            self.path = Path(
                os.getenv("DATA_PATH", str(self.path))).expanduser()
        if os.getenv("LOG_LEVEL"):
            # type: ignore[assignment]
            self.log_level = os.getenv("LOG_LEVEL", self.log_level)

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        result: Dict[str, Any] = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if isinstance(val, Path):
                result[f.name] = str(val)
            else:
                result[f.name] = val
        return result

    @staticmethod
    def _cast_env_value(value: str, annotation: Any) -> Any:
        origin = get_origin(annotation)
        args = get_args(annotation)

        target_type = annotation
        if origin is Optional:
            target_type = args[0]

        # Handle common types
        if target_type is bool:
            return value.strip().lower() in {"1", "true", "yes", "on"}
        if target_type is int:
            try:
                return int(value)
            except ValueError:
                return value
        if target_type is float:
            try:
                return float(value)
            except ValueError:
                return value
        if target_type is Path:
            return Path(value).expanduser()
        # Fallback to string
        return value
