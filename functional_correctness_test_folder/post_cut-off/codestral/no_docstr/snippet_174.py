
import json
from typing import Any
import boto3


class Configuration:

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    @property
    def bedrock_client(self) -> Any:
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client(
                'bedrock-runtime', region_name=self.region)
        return self._bedrock_client
