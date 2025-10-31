
import json
from typing import Any, Dict
import boto3


class Configuration:
    """Manages configuration for the MCP client and the Bedrock client."""

    def __init__(self, model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0', region='us-west-2') -> None:
        """Initialize configuration."""
        self.model_id = model_id
        self.region = region

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Configuration file '{file_path}' not found.") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in configuration file '{file_path}'.", e.doc, e.pos) from e

    @property
    def bedrock_client(self) -> Any:
        """Get a Bedrock runtime client.

        Returns:
            The Bedrock client.
        """
        return boto3.client('bedrock-runtime', region_name=self.region)
