
import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError


class Configuration:
    """Manages configuration for the MCP client and the Bedrock client."""

    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2") -> None:
        """Initialize configuration."""
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            json.JSONDecodeError: If configuration file is invalid JSON.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def bedrock_client(self) -> Any:
        """Get a Bedrock runtime client.

        Returns:
            The Bedrock client.
        """
        if self._bedrock_client is None:
            try:
                self._bedrock_client = boto3.client(
                    "bedrock-runtime",
                    region_name=self.region,
                )
            except (BotoCoreError, NoCredentialsError) as exc:
                raise RuntimeError(
                    f"Failed to create Bedrock client: {exc}") from exc
        return self._bedrock_client
