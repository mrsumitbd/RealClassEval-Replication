from typing import Any, Optional
import json
import os

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # type: ignore


class Configuration:
    def __init__(self, model_id: str = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0', region: str = 'us-west-2') -> None:
        if not isinstance(model_id, str) or not model_id.strip():
            raise ValueError("model_id must be a non-empty string")
        if not isinstance(region, str) or not region.strip():
            raise ValueError("region must be a non-empty string")
        self.model_id: str = model_id
        self.region: str = region
        self._bedrock_client: Optional[Any] = None

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string")

        path = os.path.expanduser(os.path.expandvars(file_path))
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Configuration file not found: {path}")

        _, ext = os.path.splitext(path)
        ext = ext.lower()

        with open(path, "r", encoding="utf-8") as f:
            if ext == ".json":
                data = json.load(f)
            elif ext in (".yaml", ".yml"):
                if yaml is None:
                    raise ImportError(
                        "PyYAML is required to load YAML configuration files")
                data = yaml.safe_load(f)  # type: ignore
            else:
                raise ValueError(
                    f"Unsupported configuration file extension: {ext}")

        if data is None:
            return {}
        if not isinstance(data, dict):
            raise TypeError("Configuration content must be a mapping (object)")

        return data  # type: ignore[return-value]

    @property
    def bedrock_client(self) -> Any:
        if self._bedrock_client is None:
            try:
                import boto3  # type: ignore
            except Exception as e:
                raise ImportError(
                    "boto3 is required to create a Bedrock client") from e
            self._bedrock_client = boto3.client(
                "bedrock-runtime", region_name=self.region)
        return self._bedrock_client
