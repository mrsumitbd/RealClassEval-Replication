
import os
import json
from typing import Any


class Configuration:

    def __init__(self) -> None:
        self._llm_api_key = None

    @staticmethod
    def load_env() -> None:
        from dotenv import load_dotenv
        load_dotenv()

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        with open(file_path, 'r') as file:
            return json.load(file)

    @property
    def llm_api_key(self) -> str:
        if self._llm_api_key is None:
            self._llm_api_key = os.getenv('LLM_API_KEY')
        return self._llm_api_key
