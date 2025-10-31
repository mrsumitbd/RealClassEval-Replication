from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Type, TypeVar
import yaml
import os

T = TypeVar('T', bound='InferenceConfig')


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    # Example fields (add or modify as needed)
    model_path: str = ''
    batch_size: int = 1
    device: str = 'cpu'
    num_workers: int = 0
    other_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if not isinstance(self.model_path, str):
            raise ValueError("model_path must be a string")
        if not isinstance(self.batch_size, int) or self.batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        if self.device not in ('cpu', 'cuda'):
            raise ValueError("device must be 'cpu' or 'cuda'")
        if not isinstance(self.num_workers, int) or self.num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer")
        if not isinstance(self.other_params, dict):
            raise ValueError("other_params must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        '''Create a configuration instance from a dictionary.'''
        # Separate known fields and other_params
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        known = {k: v for k, v in config_dict.items() if k in field_names}
        extras = {k: v for k, v in config_dict.items() if k not in field_names}
        if 'other_params' in known and isinstance(known['other_params'], dict):
            known['other_params'] = {**known['other_params'], **extras}
        else:
            known['other_params'] = extras
        return cls(**known)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str) -> T:
        '''Load configuration from a YAML file.'''
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(self.to_dict(), f, default_flow_style=False)
