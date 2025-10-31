
import os
import json
from typing import Any


class Configuration:

    def __init__(self) -> None:
        self._llm_api_key = None
        self.load_env()

    @staticmethod
    def load_env() -> None:
        try:
            with open('.env', 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except FileNotFoundError:
            pass

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    @property
    def llm_api_key(self) -> str:
        if self._llm_api_key is None:
            self._llm_api_key = os.environ.get('LLM_API_KEY')
        return self._llm_api_key
