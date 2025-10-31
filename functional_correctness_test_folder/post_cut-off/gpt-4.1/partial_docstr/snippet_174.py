
from typing import Any
import json
import os


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @property
    def bedrock_client(self) -> Any:
        if self._bedrock_client is None:
            try:
                import boto3
            except ImportError:
                raise ImportError(
                    "boto3 is required to create a Bedrock client.")
            self._bedrock_client = boto3.client(
                'bedrock-runtime', region_name=self.region)
        return self._bedrock_client
