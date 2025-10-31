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
        '''Load environment variables from .env file.'''
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            return

        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if line.startswith('export '):
                        line = line[len('export '):].strip()
                    if '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    if value and value[0] in ('"', "'") and value[-1:] == value[0]:
                        value = value[1:-1]
                    else:
                        if '#' in value:
                            value = value.split('#', 1)[0].rstrip()

                    value = os.path.expandvars(value)
                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            # Silently ignore file access/read issues
            pass

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
                f"Configuration file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Configuration file must contain a JSON object")
        return data

    @property
    def llm_api_key(self) -> str:
        '''Get the LLM API key.
        Returns:
            The API key as a string.
        Raises:
            ValueError: If the API key is not found in environment variables.
        '''
        candidates = [
            'LLM_API_KEY',
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'GOOGLE_API_KEY',
            'GEMINI_API_KEY',
            'MISTRAL_API_KEY',
            'COHERE_API_KEY',
            'TOGETHER_API_KEY',
            'GROQ_API_KEY',
            'AZURE_OPENAI_API_KEY',
        ]
        for var in candidates:
            value = os.environ.get(var)
            if value:
                return value
        raise ValueError(
            "LLM API key not found in environment variables. "
            f"Set one of: {', '.join(candidates)}"
        )
