
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any
import yaml
import os


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        self._validate_and_adjust()

    def _validate_and_adjust(self):
        # Example validation and adjustment logic
        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not isinstance(self.model_path, str) or not os.path.exists(self.model_path):
            raise ValueError("model_path must be a valid path")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
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
