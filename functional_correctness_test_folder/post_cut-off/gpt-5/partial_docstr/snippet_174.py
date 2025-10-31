from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id: str = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', region: str = 'us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id: str = model_id
        self.region: str = region
        self._config: Dict[str, Any] = {}
        self._bedrock_client: Optional[Any] = None

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        if not file_path:
            raise ValueError("file_path must be a non-empty string")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        _, ext = os.path.splitext(file_path.lower())
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if ext in (".json", ""):
                    data = json.load(f)
                elif ext in (".yml", ".yaml"):
                    try:
                        import yaml  # type: ignore
                    except Exception as e:
                        raise ImportError(
                            "PyYAML is required to load YAML configuration files") from e
                    data = yaml.safe_load(f) or {}
                else:
                    raise ValueError(
                        f"Unsupported configuration file extension: {ext}")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in configuration file: {file_path}") from e

        if not isinstance(data, dict):
            raise ValueError(
                "Configuration file content must be a JSON/YAML object")
        return data  # type: ignore[return-value]

    @property
    def bedrock_client(self) -> Any:
        if self._bedrock_client is None:
            try:
                import boto3  # type: ignore
            except Exception as e:
                raise ImportError(
                    "boto3 is required to create a Bedrock client") from e

            region = self.region or os.environ.get(
                "AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
            if not region:
                raise ValueError(
                    "AWS region is not specified. Set it in Configuration or via AWS_REGION/AWS_DEFAULT_REGION.")

            self._bedrock_client = boto3.client(
                "bedrock-runtime", region_name=region)
        return self._bedrock_client
