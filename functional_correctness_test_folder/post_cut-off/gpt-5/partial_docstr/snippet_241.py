from __future__ import annotations

import json
import os
from json import JSONDecodeError
from typing import Any


class Configuration:
    '''Manages configuration and environment variables for the MCP client.'''

    def __init__(self) -> None:
        '''Initialize configuration with environment variables.'''
        self.load_env()
        self._env: dict[str, str] = dict(os.environ)

    @staticmethod
    def load_env() -> None:
        """
        Load environment variables from the nearest .env file without overriding existing vars.
        The search starts in the current working directory and walks up to the filesystem root.
        Supported line formats:
          - KEY=value
          - export KEY=value
        Values may be wrapped in single or double quotes.
        Lines starting with '#' or blank lines are ignored.
        """
        def find_dotenv(start_dir: str) -> str | None:
            current = os.path.abspath(start_dir)
            root = os.path.abspath(os.sep)
            while True:
                candidate = os.path.join(current, ".env")
                if os.path.isfile(candidate):
                    return candidate
                if current == root:
                    return None
                current = os.path.dirname(current)

        path = find_dotenv(os.getcwd())
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("export "):
                        line = line[len("export "):].lstrip()
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    value = value.replace("\\n", "\n").replace(
                        "\\t", "\t").replace("\\r", "\r")

                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            # If the .env file cannot be read, silently skip loading.
            return

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
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise JSONDecodeError(
                "Top-level JSON must be an object", doc=str(data), pos=0)
        return data

    @property
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        priorities = [
            "LLM_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "GOOGLE_API_KEY",
            "AZURE_OPENAI_API_KEY",
        ]
        for key in priorities:
            value = self._env.get(key) or os.environ.get(key)
            if value:
                return value
        raise ValueError(
            "LLM API key not found in environment variables. "
            "Set one of: LLM_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, AZURE_OPENAI_API_KEY."
        )
