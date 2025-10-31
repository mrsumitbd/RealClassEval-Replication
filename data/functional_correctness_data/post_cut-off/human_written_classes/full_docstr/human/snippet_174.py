from typing import Any
import json
from botocore.config import Config
import boto3

class Configuration:
    """Manages configuration for the MCP client and the Bedrock client."""

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        """Initialize configuration."""
        self.model_id = model_id
        self.region = region

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        """Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
        """
        with open(file_path, 'r') as f:
            return json.load(f)

    @property
    def bedrock_client(self) -> Any:
        """Get a Bedrock runtime client.

        Returns:
            The Bedrock client.
        """
        retry_config = Config(retries={'max_attempts': 10, 'mode': 'standard'})
        return boto3.client('bedrock-runtime', region_name=self.region, config=retry_config)