
from __future__ import annotations

import yaml
from dataclasses import dataclass, asdict
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    """
    A generic configuration holder for inference settings.
    Users can extend this class with additional fields as needed.
    """

    def __post_init__(self) -> None:
        """
        Hook that runs after the dataclass is initialized.
        Subclasses may override this method to perform validation.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a plain dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        """
        Create an instance of the configuration from a dictionary.
        """
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str) -> T:
        """
        Load configuration from a YAML file.
        """
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(
                f"YAML file {yaml_path} does not contain a mapping.")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        """
        Save the configuration to a YAML file.
        """
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f,
                           default_flow_style=False, sort_keys=False)
