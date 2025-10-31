
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any
import yaml


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        '''Create a configuration instance from a dictionary.'''
        field_names = {f.name for f in fields(cls)}
        filtered_dict = {k: v for k, v in config_dict.items()
                         if k in field_names}
        return cls(**filtered_dict)

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
