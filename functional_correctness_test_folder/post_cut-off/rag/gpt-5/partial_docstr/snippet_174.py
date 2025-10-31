import json
import os
from typing import Any


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'
        '''
        self.model_id = model_id
        self.region = region
        self._bedrock_client: Any = None

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
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f'Configuration file not found: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(
                'Configuration file must contain a top-level JSON object.')
        return data

    @property
    def bedrock_client(self) -> Any:
        '''Get a Bedrock runtime client.
        Returns:
            The Bedrock client.
        '''
        if self._bedrock_client is None:
            try:
                import boto3
            except Exception as e:
                raise ImportError(
                    'boto3 is required to create a Bedrock client.') from e
            self._bedrock_client = boto3.client(
                'bedrock-runtime', region_name=self.region)
        return self._bedrock_client
