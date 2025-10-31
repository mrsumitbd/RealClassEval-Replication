
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

import yaml

T = TypeVar("T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    # NOTE: The concrete configuration fields are defined by subclasses or
    # by the user when instantiating the dataclass.  The base class only
    # provides generic helpers for serialisation and validation.

    def __post_init__(self) -> None:
        """Validate and adjust configuration after initialization."""
        # Subclasses may override this method to perform custom validation.
        # The base implementation does nothing.
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        """Create a configuration instance from a dictionary."""
        # The base implementation simply forwards the dictionary to the
        # dataclass constructor.  Subclasses may override to perform
        # additional processing.
        return cls(**config_dict)  # type: ignore[arg-type]

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str | Path) -> T:
        """Load configuration from a YAML file."""
        path = Path(yaml_path)
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with path.open("rt", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"YAML file {path} does not contain a mapping")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str | Path) -> None:
        """Save configuration to a YAML file."""
        path = Path(yaml_path)
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wt", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f,
                           default_flow_style=False, sort_keys=False)
