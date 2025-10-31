
import os
import json
from typing import Any


class Configuration:
    '''Manages configuration and environment variables for the MCP client.'''

    def __init__(self) -> None:
        '''Initialize configuration with environment variables.'''
        self._env = dict(os.environ)

    @staticmethod
    def load_env() -> None:
        '''Load environment variables from .env file.'''
        dotenv_path = ".env"
        if not os.path.exists(dotenv_path):
            return
        with open(dotenv_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        '''Load server configuration from JSON file.
        Args:
            file_path: Path to the JSON configuration file.
        Returns:
            Dict containing server configuration.
        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
        '''
        with open(file_path, "r") as f:
            return json.load(f)

    @property
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        key = self._env.get("LLM_API_KEY") or os.environ.get("LLM_API_KEY")
        if not key:
            raise ValueError("LLM_API_KEY not found in environment variables.")
        return key
