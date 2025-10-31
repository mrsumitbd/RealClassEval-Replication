from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Type, TypeVar
import yaml
import os

T = TypeVar('T', bound='InferenceConfig')


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    # Example fields (add or modify as needed)
    batch_size: int = 32
    device: str = "cpu"
    num_workers: int = 4
    model_path: str = ""
    output_dir: str = "./outputs"
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.num_workers < 0:
            raise ValueError("num_workers cannot be negative")
        if not self.device:
            self.device = "cpu"
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        if not isinstance(self.extra, dict):
            raise ValueError("extra must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        '''Create a configuration instance from a dictionary.'''
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str) -> T:
        '''Load configuration from a YAML file.'''
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        with open(yaml_path, "w") as f:
            yaml.safe_dump(self.to_dict(), f, default_flow_style=False)
