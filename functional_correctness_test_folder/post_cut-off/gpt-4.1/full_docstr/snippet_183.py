
from dataclasses import dataclass, field, asdict
from typing import Any, Dict
import yaml
import os


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    batch_size: int = 32
    device: str = "cpu"
    num_workers: int = 4
    precision: str = "fp32"
    model_path: str = ""
    output_path: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.num_workers < 0:
            raise ValueError("num_workers cannot be negative")
        if self.precision not in ("fp32", "fp16", "int8"):
            raise ValueError(
                "precision must be one of: 'fp32', 'fp16', 'int8'")
        if not isinstance(self.extra, dict):
            raise TypeError("extra must be a dictionary")
        # Optionally, expand ~ in paths
        self.model_path = os.path.expanduser(self.model_path)
        self.output_path = os.path.expanduser(self.output_path)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        '''Create a configuration instance from a dictionary.'''
        # Separate known fields and extra
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        known = {k: v for k, v in config_dict.items() if k in field_names}
        extra = {k: v for k, v in config_dict.items() if k not in field_names}
        if 'extra' in known and isinstance(known['extra'], dict):
            known['extra'] = {**known['extra'], **extra}
        else:
            known['extra'] = extra
        return cls(**known)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        '''Load configuration from a YAML file.'''
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(self.to_dict(), f)
