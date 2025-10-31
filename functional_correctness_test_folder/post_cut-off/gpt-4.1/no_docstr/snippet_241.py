
import os
import json
from typing import Any


class Configuration:

    def __init__(self) -> None:
        self._config = {}
        self._api_key = None

    @staticmethod
    def load_env() -> None:
        from dotenv import load_dotenv
        load_dotenv()

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    @property
    def llm_api_key(self) -> str:
        if self._api_key is not None:
            return self._api_key
        api_key = os.environ.get("LLM_API_KEY")
        if api_key:
            self._api_key = api_key
            return api_key
        if self._config and "llm_api_key" in self._config:
            self._api_key = self._config["llm_api_key"]
            return self._api_key
        return ""
