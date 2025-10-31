
import os
import json
from json import JSONDecodeError
from typing import Any, Dict

try:
    # Optional: use python-dotenv if available
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
        if load_dotenv is not None:
            load_dotenv()
        # If dotenv is not available, rely on existing environment variables

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """
        Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def llm_api_key(self) -> str:
        """
        Get the LLM API key.

        Returns:
            The API key as a string.

        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        key = os.getenv("LLM_API_KEY")
        if not key:
            raise ValueError("LLM_API_KEY environment variable is not set")
        return key
