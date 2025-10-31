
import json
from pathlib import Path
from typing import Any, Dict

import boto3


class Configuration:
    def __init__(self, model_id: str = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', region: str = 'us-west-2') -> None:
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """
        Load a JSON configuration file and return its contents as a dictionary.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)

    @property
    def bedrock_client(self) -> Any:
        """
        Lazily create and return a Bedrock runtime client.
        """
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client(
                'bedrock-runtime', region_name=self.region)
        return self._bedrock_client
