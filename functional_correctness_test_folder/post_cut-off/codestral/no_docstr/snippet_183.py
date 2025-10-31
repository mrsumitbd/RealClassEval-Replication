
from dataclasses import dataclass, asdict
from typing import Dict, Any
import yaml


@dataclass
class InferenceConfig:

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        with open(yaml_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        with open(yaml_path, 'w') as file:
            yaml.dump(self.to_dict(), file)
