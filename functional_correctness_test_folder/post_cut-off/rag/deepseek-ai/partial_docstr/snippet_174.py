
import json
from typing import Any, Dict


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id = model_id
        self.region = region

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
        with open(file_path, 'r') as f:
            config = json.load(f)
        return config

    @property
    def bedrock_client(self) -> Any:
        '''Get a Bedrock runtime client.
        Returns:
            The Bedrock client.
        '''
        import boto3
        return boto3.client('bedrock-runtime', region_name=self.region)
