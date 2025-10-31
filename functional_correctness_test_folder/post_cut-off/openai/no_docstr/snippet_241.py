
import os
import json
from typing import Any, Dict

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    import yaml
except ImportError:
    yaml = None


class Configuration:
    def __init__(self) -> None:
        self._config: Dict[str, Any] = {}
        self._env_loaded: bool = False

    @staticmethod
    def load_env() -> None:
        """Load environment variables from a .env file if available."""
        if load_dotenv is not None:
            load_dotenv()
        else:
            # If python-dotenv is not installed, silently ignore
            pass

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """Load configuration from a JSON or YAML file."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        _, ext = os.path.splitext(file_path.lower())
        with open(file_path, "r", encoding="utf-8") as f:
            if ext in {".json"}:
                return json.load(f)
            elif ext in {".yaml", ".yml"}:
                if yaml is None:
                    raise ImportError(
                        "PyYAML is required to load YAML configuration files.")
                return yaml.safe_load(f) or {}
            else:
                raise ValueError(
                    f"Unsupported configuration file format: {ext}")

    @property
    def llm_api_key(self) -> str:
        """Return the LLM API key from environment or configuration."""
        # Load environment variables if not already loaded
        if not self._env_loaded:
            self.load_env()
            self._env_loaded = True

        key = os.getenv("LLM_API_KEY")
        if key:
            return key

        # Fallback to configuration dictionary
        key = self._config.get("llm_api_key")
        if key:
            return key

        raise ValueError(
            "LLM_API_KEY not found in environment variables or configuration.")
