
import os
import json
from typing import Any


class Configuration:
    '''Manages configuration and environment variables for the MCP client.'''

    def __init__(self) -> None:
        '''Initialize configuration with environment variables.'''
        self.load_env()

    @staticmethod
    def load_env() -> None:
        '''Load environment variables.'''
        from dotenv import load_dotenv
        load_dotenv()

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
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file {file_path} not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Invalid JSON format", doc='', pos=0)

    @property
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        api_key = os.getenv('LLM_API_KEY')
        if not api_key:
            raise ValueError("LLM API key not found in environment variables.")
        return api_key
