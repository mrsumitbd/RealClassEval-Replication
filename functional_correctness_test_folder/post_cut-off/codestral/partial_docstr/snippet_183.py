
from dataclasses import dataclass, asdict
from typing import Dict, Any
import yaml


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        pass

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
