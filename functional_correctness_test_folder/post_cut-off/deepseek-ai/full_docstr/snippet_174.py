
import json
from typing import Any, Dict
import boto3


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'''
        self._model_id = model_id
        self._region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        '''Load server configuration from JSON file.
        Args:
            file_path: Path to the JSON configuration file.
        Returns:
            Dict containing server configuration.
        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
        '''
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    @property
    def bedrock_client(self) -> Any:
        '''Get a Bedrock runtime client.
        Returns:
            The Bedrock client.
        '''
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self._region
            )
        return self._bedrock_client
