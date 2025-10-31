
import json
import os
from pathlib import Path
from typing import Any, Dict

try:
    # Try to use python-dotenv if available
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None  # type: ignore


class Configuration:
    """Manages configuration and environment variables for the MCP client."""

    def __init__(self) -> None:
        """Initialize configuration with environment variables."""
        self.load_env()

    @staticmethod
    def load_env() -> None:
        """Load environment variables from .env file."""
        # If python-dotenv is available, use it
        if load_dotenv:
            load_dotenv()
            return

        # Fallback: manually load .env if present
        env_path = Path(".env")
        if not env_path.is_file():
            return

        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            json.JSONDecodeError: If configuration file is invalid JSON.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def llm_api_key(self) -> str:
        """Get the LLM API key.

        Returns:
            The API key as a string.

        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        key = os.getenv("LLM_API_KEY")
        if not key:
            raise ValueError("LLM_API_KEY environment variable is not set")
        return key
