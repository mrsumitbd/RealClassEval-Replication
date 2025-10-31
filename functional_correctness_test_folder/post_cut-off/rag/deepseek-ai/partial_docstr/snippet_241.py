
import json
import os
from typing import Any, Dict


class Configuration:
    '''Manages configuration and environment variables for the MCP client.'''

    def __init__(self) -> None:
        '''Initialize configuration with environment variables.'''
        self._llm_api_key = os.getenv('LLM_API_KEY')

    @staticmethod
    def load_env() -> None:
        '''Load environment variables from .env file.'''
        from dotenv import load_dotenv
        load_dotenv()

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
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        if self._llm_api_key is None:
            raise ValueError('LLM_API_KEY not found in environment variables')
        return self._llm_api_key
