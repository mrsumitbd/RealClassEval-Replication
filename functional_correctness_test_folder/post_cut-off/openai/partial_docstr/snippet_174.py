
import json
import os
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError


class Configuration:
    '''Manages configuration for the MCP client and the Bedrock client.'''

    def __init__(self, model_id: str = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
                 region: str = 'us-west-2') -> None:
        '''Initialize configuration.'''
        self.model_id = model_id
        self.region = region
        self._bedrock_client = None
        self._config: Dict[str, Any] = {}

    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        '''Load configuration from a JSON or YAML file.'''
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}")

        _, ext = os.path.splitext(file_path.lower())
        with open(file_path, 'r', encoding='utf-8') as f:
            if ext in {'.yaml', '.yml'}:
                if yaml is None:
                    raise ImportError(
                        "PyYAML is required to load YAML configuration files.")
                return yaml.safe_load(f) or {}
            elif ext == '.json':
                return json.load(f)
            else:
                raise ValueError(
                    f"Unsupported configuration file format: {ext}")

    @property
    def bedrock_client(self) -> Any:
        '''Return a lazily‑created Bedrock runtime client.'''
        if self._bedrock_client is None:
            try:
                self._bedrock_client = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region
                )
            except (BotoCoreError, NoCredentialsError) as exc:
                raise RuntimeError("Failed to create Bedrock client") from exc
        return self._bedrock_client
