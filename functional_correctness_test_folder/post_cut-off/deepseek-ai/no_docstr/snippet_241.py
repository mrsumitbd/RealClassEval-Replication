
import os
import json
from typing import Any, Dict


class Configuration:

    def __init__(self) -> None:
        self._llm_api_key = ""

    @staticmethod
    def load_env() -> None:
        from dotenv import load_dotenv
        load_dotenv()

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    @property
    def llm_api_key(self) -> str:
        return self._llm_api_key
