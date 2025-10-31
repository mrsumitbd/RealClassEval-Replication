from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class Configuration:
    '''Manages configuration and environment variables for the MCP client.'''

    def __init__(self) -> None:
        '''Initialize configuration with environment variables.'''
        self.load_env()
        self._env = os.environ

    @staticmethod
    def load_env() -> None:
        '''Load environment variables from .env file.'''
        # Try python-dotenv if available
        try:
            from dotenv import load_dotenv as _load_dotenv  # type: ignore
            _load_dotenv(override=False)
            return
        except Exception:
            pass

        # Fallback: manual .env loading from current dir upwards
        def _find_env_file(start: Path) -> Path | None:
            for parent in [start, *start.parents]:
                candidate = parent / ".env"
                if candidate.is_file():
                    return candidate
            return None

        env_path = _find_env_file(Path.cwd())
        if not env_path:
            return

        try:
            with env_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    # Remove optional surrounding quotes
                    value = value.strip().strip("'").strip('"')
                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            # Silently ignore issues reading .env
            pass

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
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        candidates = [
            "LLM_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "GEMINI_API_KEY",
            "MISTRAL_API_KEY",
            "COHERE_API_KEY",
            "TOGETHER_API_KEY",
        ]
        for key in candidates:
            val = self._env.get(key)
            if val:
                return val
        raise ValueError(
            "LLM API key not found in environment. Checked: "
            + ", ".join(candidates)
        )
