import json
from dataclasses import dataclass, field
from dotenv import load_dotenv
from decouple import config as decouple_config
from pathlib import Path
from omnicoreagent.core.utils import logger

@dataclass
class Configuration:
    """Manages configuration and environment variables for the MCP client."""
    llm_api_key: str = field(init=False)
    embedding_api_key: str = field(init=False)

    def __post_init__(self) -> None:
        """Initialize configuration with environment variables."""
        self.load_env()
        self.llm_api_key = decouple_config('LLM_API_KEY', default=None)
        self.embedding_api_key = decouple_config('EMBEDDING_API_KEY', default=None)
        if not self.llm_api_key:
            raise ValueError('LLM_API_KEY not found in environment variables')

    @staticmethod
    def load_env() -> None:
        """Load environment variables from .env file."""
        load_dotenv()

    def load_config(self, file_path: str) -> dict:
        """Load server configuration from JSON file."""
        config_path = Path(file_path)
        logger.info(f'Loading configuration from: {config_path.name}')
        if not config_path.name.startswith('servers_config'):
            raise ValueError("Config file name must start with 'servers_config'")
        if config_path.is_absolute() or config_path.parent != Path('.'):
            if config_path.exists():
                with open(config_path, encoding='utf-8') as f:
                    return json.load(f)
            else:
                raise FileNotFoundError(f'Configuration file not found: {config_path}')
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                return json.load(f)
        raise FileNotFoundError(f'Configuration file not found: {config_path}')