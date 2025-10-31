
from __future__ import annotations

import yaml
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    # NOTE: The actual configuration fields are defined elsewhere.
    # This skeleton only implements the helper methods.

    def __post_init__(self) -> None:
        """Validate and adjust configuration after initialization."""
        # Basic validation: ensure that the instance can be converted to a dict
        # and that it contains at least one field.  Sub‑classes may override
        # this method to perform more specific checks.
        if not hasattr(self, "__dict__"):
            raise ValueError(
                "InferenceConfig must be a dataclass with fields.")
        # If the dataclass has no fields, raise an error to avoid silent misuse.
        if not self.__dict__:
            raise ValueError(
                "InferenceConfig must have at least one field defined.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        # Use dataclasses.asdict to handle nested dataclasses correctly.
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        """Create a configuration instance from a dictionary."""
        if not isinstance(config_dict, dict):
            raise TypeError("config_dict must be a dictionary")
        return cls(**config_dict)  # type: ignore[arg-type]

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str | Path) -> T:
        """Load configuration from a YAML file."""
        path = Path(yaml_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"YAML file not found: {path}")
        with path.open("rt", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"YAML file {path} does not contain a mapping")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str | Path) -> None:
        """Save configuration to a YAML file."""
        path = Path(yaml_path).expanduser().resolve()
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wt", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f,
                           default_flow_style=False, sort_keys=False)
