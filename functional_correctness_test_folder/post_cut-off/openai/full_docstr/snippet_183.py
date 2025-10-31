
from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from typing import Any, Dict

import yaml


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    model_path: str
    batch_size: int = 1
    device: str = "cpu"
    output_dir: str = "./outputs"
    use_fp16: bool = False
    max_seq_length: int = 512

    def __post_init__(self) -> None:
        """Validate and adjust configuration after initialization."""
        if not isinstance(self.model_path, str) or not self.model_path:
            raise ValueError("model_path must be a non-empty string")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model path does not exist: {self.model_path}")

        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")

        if self.device not in {"cpu", "cuda"}:
            raise ValueError("device must be either 'cpu' or 'cuda'")

        if not isinstance(self.output_dir, str) or not self.output_dir:
            raise ValueError("output_dir must be a non-empty string")

        if not isinstance(self.use_fp16, bool):
            raise ValueError("use_fp16 must be a boolean")

        if not isinstance(self.max_seq_length, int) or self.max_seq_length <= 0:
            raise ValueError("max_seq_length must be a positive integer")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "InferenceConfig":
        """Create a configuration instance from a dictionary."""
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "InferenceConfig":
        """Load configuration from a YAML file."""
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(
                "YAML file must contain a mapping at the top level")

        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        """Save configuration to a YAML file."""
        dir_name = os.path.dirname(yaml_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, default_flow_style=False)
