
import json
import os
from json import JSONDecodeError
from typing import Any, Dict

try:
    # Optional dependency – only used if available
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


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
        else:
            # Fallback: manually read a .env file if present
            env_path = ".env"
            if os.path.isfile(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" not in line:
                            continue
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())

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
        if key is None:
            raise ValueError("LLM_API_KEY environment variable is not set")
        return key
