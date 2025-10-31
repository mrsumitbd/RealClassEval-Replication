
from dataclasses import dataclass, asdict
from typing import Dict, Any
import yaml


@dataclass
class InferenceConfig:
    model_name: str
    batch_size: int
    max_length: int
    temperature: float

    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")
        if self.max_length <= 0:
            raise ValueError("max_length must be greater than 0")
        if not (0 < self.temperature <= 1):
            raise ValueError("temperature must be between 0 and 1")

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
