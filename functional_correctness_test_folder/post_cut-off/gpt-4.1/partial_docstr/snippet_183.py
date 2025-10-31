
from dataclasses import dataclass, asdict, field
from typing import Any, Dict
import yaml
import os


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    batch_size: int = 32
    device: str = "cpu"
    num_workers: int = 4
    model_path: str = ""
    output_dir: str = "./outputs"
    verbose: bool = False

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.num_workers < 0:
            raise ValueError("num_workers cannot be negative")
        if not isinstance(self.device, str):
            raise TypeError("device must be a string")
        if not isinstance(self.model_path, str):
            raise TypeError("model_path must be a string")
        if not isinstance(self.output_dir, str):
            raise TypeError("output_dir must be a string")
        if not isinstance(self.verbose, bool):
            raise TypeError("verbose must be a boolean")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(self.to_dict(), f)
