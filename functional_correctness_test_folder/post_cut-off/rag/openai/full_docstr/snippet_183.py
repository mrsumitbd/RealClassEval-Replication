
from __future__ import annotations

import yaml
from dataclasses import dataclass, asdict, fields
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    # NOTE: The actual configuration fields are defined elsewhere in the
    # project.  This implementation works for any dataclass that inherits
    # from InferenceConfig.

    def __post_init__(self) -> None:
        """
        Validate and adjust configuration after initialization.

        The base implementation performs no validation.  Sub‑classes may
        override this method to enforce constraints (e.g. positive
        integers, mutually exclusive options, etc.).
        """
        # Example placeholder for validation logic:
        # for f in fields(self):
        #     value = getattr(self, f.name)
        #     if value is None:
        #         raise ValueError(f"Configuration field '{f.name}' cannot be None")
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.

        Returns:
            A plain dictionary representation of the dataclass.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        """
        Create a configuration instance from a dictionary.

        Args:
            config_dict: Mapping of field names to values.

        Returns:
            An instance of ``InferenceConfig`` (or a subclass).
        """
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str | Path) -> T:
        """
        Load configuration from a YAML file.

        Args:
            yaml_path: Path to the YAML file.

        Returns:
            An instance of ``InferenceConfig`` (or a subclass).
        """
        path = Path(yaml_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with path.open("rt", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"YAML file {path} does not contain a mapping")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str | Path) -> None:
        """
        Save configuration to a YAML file.

        Args:
            yaml_path: Destination file path.
        """
        path = Path(yaml_path).expanduser().resolve()
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wt", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f,
                           default_flow_style=False, sort_keys=False)
