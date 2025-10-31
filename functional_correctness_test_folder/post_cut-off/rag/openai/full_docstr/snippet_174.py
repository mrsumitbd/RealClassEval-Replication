
import json
from pathlib import Path
from typing import Any, Dict

import boto3


class Configuration:
    """Manages configuration for the MCP client and the Bedrock client."""

    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2") -> None:
        """Initialize configuration."""
        self.model_id = model_id
        self.region = region

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """
        Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            json.JSONDecodeError: If configuration file is invalid JSON.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def bedrock_client(self) -> Any:
        """
        Get a Bedrock runtime client.

        Returns:
            The Bedrock client.
        """
        return boto3.client("bedrock-runtime", region_name=self.region)
