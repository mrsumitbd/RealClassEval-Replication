
import boto3
import json
from typing import Any


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse configuration file '{file_path}': {e}")

    @property
    def bedrock_client(self) -> Any:
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client(
                'bedrock-runtime', region_name=self.region)
        return self._bedrock_client
