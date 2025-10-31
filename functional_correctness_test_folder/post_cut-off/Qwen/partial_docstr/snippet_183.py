
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any
import yaml
import os


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    model_path: str
    batch_size: int
    device: str

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if not os.path.exists(self.model_path):
            raise ValueError(f"Model path {self.model_path} does not exist.")
        if self.batch_size <= 0:
            raise ValueError("Batch size must be a positive integer.")
        if self.device not in ['cpu', 'cuda']:
            raise ValueError("Device must be either 'cpu' or 'cuda'.")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        '''Create a configuration instance from a dictionary.'''
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        '''Load configuration from a YAML file.'''
        with open(yaml_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        with open(yaml_path, 'w') as file:
            yaml.dump(self.to_dict(), file)
