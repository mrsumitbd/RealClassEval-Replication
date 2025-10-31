
import json
from typing import Any, Dict
import boto3


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id = model_id
        self.region = region
        self.config = {}

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
        try:
            with open(file_path, 'r') as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{file_path}' not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                "Invalid JSON format in configuration file.", doc='', pos=0)

    @property
    def bedrock_client(self) -> Any:
        '''Get a Bedrock runtime client.
        Returns:
            The Bedrock client.
        '''
        if not self.config:
            raise ValueError(
                "Configuration not loaded. Please load the configuration first using load_config.")
        return boto3.client('bedrock', region_name=self.region, **self.config)
