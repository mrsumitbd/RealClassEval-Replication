
from dataclasses import dataclass, asdict, fields
from typing import Any, Dict
import yaml


@dataclass
class InferenceConfig:
    # Example fields; you can modify/add as needed
    batch_size: int = 32
    device: str = "cpu"
    num_workers: int = 4
    model_path: str = ""
    threshold: float = 0.5

    def __post_init__(self):
        # Ensure types are correct
        self.batch_size = int(self.batch_size)
        self.device = str(self.device)
        self.num_workers = int(self.num_workers)
        self.model_path = str(self.model_path)
        self.threshold = float(self.threshold)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        field_names = {f.name for f in fields(cls)}
        filtered_dict = {k: v for k, v in config_dict.items()
                         if k in field_names}
        return cls(**filtered_dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)

    def save_yaml(self, yaml_path: str) -> None:
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(self.to_dict(), f)
