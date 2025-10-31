
from dataclasses import dataclass, asdict
from typing import Dict, Any
import yaml


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    # Add fields here, for example:
    # model_path: str
    # batch_size: int
    # num_workers: int

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        # Add validation logic here, for example:
        # if self.batch_size <= 0:
        #     raise ValueError("Batch size must be positive")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        '''Create a configuration instance from a dictionary.'''
        return cls(**config_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        '''Load configuration from a YAML file.'''
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        config_dict = self.to_dict()
        with open(yaml_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)

# Example usage:


@dataclass
class InferenceConfig:
    model_path: str
    batch_size: int
    num_workers: int

    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")
        if self.num_workers < 0:
            raise ValueError("Number of workers must be non-negative")


# Test the class
if __name__ == "__main__":
    config = InferenceConfig(model_path="path/to/model",
                             batch_size=32, num_workers=4)
    print(config.to_dict())

    config_dict = config.to_dict()
    config_from_dict = InferenceConfig.from_dict(config_dict)
    print(config_from_dict)

    config.save_yaml("config.yaml")
    config_from_yaml = InferenceConfig.from_yaml("config.yaml")
    print(config_from_yaml)
