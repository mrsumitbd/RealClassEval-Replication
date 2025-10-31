
from __future__ import annotations

import yaml
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    # Example fields – users can extend this dataclass with more specific settings.
    model_path: str | None = None
    device: str = "cpu"
    batch_size: int = 1
    output_dir: str = "./output"
    max_seq_length: int = 512
    use_fp16: bool = False

    def __post_init__(self) -> None:
        """Validate and adjust configuration after initialization."""
        # Basic validation
        if self.model_path is None:
            raise ValueError("`model_path` must be specified.")
        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            raise ValueError("`batch_size` must be a positive integer.")
        if self.device not in {"cpu", "cuda", "mps"}:
            raise ValueError(f"Unsupported device: {self.device!r}. "
                             "Supported devices are 'cpu', 'cuda', and 'mps'.")
        if not isinstance(self.max_seq_length, int) or self.max_seq_length <= 0:
            raise ValueError("`max_seq_length` must be a positive integer.")

    def to_dict(self) -> Dict[str, Any]:
        """Return the configuration as a plain dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        """Create a configuration instance from a dictionary."""
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str) -> T:
        """Load configuration from a YAML file."""
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(
                "YAML file must contain a mapping at the top level.")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        """Save configuration to a YAML file."""
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False)
