from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Type, TypeVar
import yaml
import os

T = TypeVar('T', bound='InferenceConfig')


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''

    # Example fields (add your own as needed)
    batch_size: int = 32
    device: str = "cpu"
    num_workers: int = 4
    model_path: str = ""
    other_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.device not in ("cpu", "cuda"):
            raise ValueError("device must be 'cpu' or 'cuda'")
        if self.num_workers < 0:
            raise ValueError("num_workers must be non-negative")
        if not isinstance(self.other_params, dict):
            raise TypeError("other_params must be a dict")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        result = asdict(self)
        return result

    @classmethod
    def from_dict(cls: Type[T], config_dict: Dict[str, Any]) -> T:
        '''Create a configuration instance from a dictionary.'''
        # Separate known fields and other_params
        field_names = set(f.name for f in cls.__dataclass_fields__.values())
        known = {k: v for k, v in config_dict.items() if k in field_names}
        extra = {k: v for k, v in config_dict.items() if k not in field_names}
        if "other_params" in known and isinstance(known["other_params"], dict):
            known["other_params"] = {**known["other_params"], **extra}
        else:
            known["other_params"] = extra
        return cls(**known)

    @classmethod
    def from_yaml(cls: Type[T], yaml_path: str) -> T:
        '''Load configuration from a YAML file.'''
        with open(yaml_path, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        with open(yaml_path, "w") as f:
            yaml.safe_dump(self.to_dict(), f)
