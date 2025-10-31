from dataclasses import dataclass, field
from typing import Dict, Any
import copy
import os
import yaml


@dataclass
class InferenceConfig:
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.config is None:
            self.config = {}
        elif not isinstance(self.config, dict):
            raise TypeError("config must be a dictionary")
        # Ensure keys are strings
        self.config = {str(k): v for k, v in self.config.items()}

    def to_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self.config)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        if config_dict is None:
            config_dict = {}
        if not isinstance(config_dict, dict):
            raise TypeError("config_dict must be a dictionary")
        return cls(config=copy.deepcopy(config_dict))

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise ValueError(
                "YAML content must be a mapping (dictionary) at the root")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(yaml_path)), exist_ok=True)
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False,
                           allow_unicode=True)
