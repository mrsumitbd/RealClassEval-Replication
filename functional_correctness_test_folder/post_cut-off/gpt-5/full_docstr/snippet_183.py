from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, TypeVar, Type
import copy
import os

_T = TypeVar("_T", bound="InferenceConfig")


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    model_name: str = "default"
    device: str = "cpu"  # e.g., "cpu", "cuda", "cuda:0"
    batch_size: int = 1
    dtype: str = "float32"  # e.g., "float32", "float16", "bfloat16"
    num_workers: int = 0
    seed: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        if not isinstance(self.model_name, str) or not self.model_name:
            raise ValueError("model_name must be a non-empty string")

        if not isinstance(self.device, str) or not self.device:
            raise ValueError("device must be a non-empty string")
        allowed_devices = {"cpu"}
        if self.device not in allowed_devices and not self.device.startswith("cuda"):
            raise ValueError(
                "device must be 'cpu' or start with 'cuda' (e.g., 'cuda', 'cuda:0')")

        if not isinstance(self.batch_size, int) or self.batch_size < 1:
            raise ValueError("batch_size must be an integer >= 1")

        if not isinstance(self.num_workers, int) or self.num_workers < 0:
            raise ValueError("num_workers must be an integer >= 0")

        allowed_dtypes = {"float32", "float16", "bfloat16"}
        if self.dtype not in allowed_dtypes:
            raise ValueError(f"dtype must be one of {sorted(allowed_dtypes)}")

        if self.seed is not None and (not isinstance(self.seed, int) or self.seed < 0):
            raise ValueError("seed must be a non-negative integer or None")

        if not isinstance(self.extra, dict):
            raise ValueError("extra must be a dictionary")

        for k in self.extra.keys():
            if not isinstance(k, str):
                raise ValueError("All keys in extra must be strings")

        # Protect against collisions: remove any keys from extra that shadow core fields
        core_fields = {"model_name", "device", "batch_size",
                       "dtype", "num_workers", "seed", "extra"}
        collisions = [
            k for k in self.extra if k in core_fields and k != "extra"]
        for k in collisions:
            self.extra.pop(k, None)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the configuration to a dictionary.'''
        data = asdict(self)
        # Merge extra into top-level for a flat representation
        extra = data.pop("extra", {}) or {}
        merged = {**data, **copy.deepcopy(extra)}
        return merged

    @classmethod
    def from_dict(cls: Type[_T], config_dict: Dict[str, Any]) -> _T:
        '''Create a configuration instance from a dictionary.'''
        if not isinstance(config_dict, dict):
            raise ValueError("config_dict must be a dictionary")

        known_keys = {"model_name", "device", "batch_size",
                      "dtype", "num_workers", "seed", "extra"}
        init_kwargs = {}
        extra: Dict[str, Any] = {}

        for k, v in config_dict.items():
            if k in known_keys and k != "extra":
                init_kwargs[k] = v
            elif k == "extra":
                if not isinstance(v, dict):
                    raise ValueError("extra must be a dictionary if provided")
                extra.update(v)
            else:
                extra[k] = v

        init_kwargs["extra"] = extra
        return cls(**init_kwargs)

    @classmethod
    def from_yaml(cls: Type[_T], yaml_path: str) -> _T:
        '''Load configuration from a YAML file.'''
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "PyYAML is required to load YAML files. Install with 'pip install pyyaml'.") from e

        if not os.path.isfile(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError("YAML content must be a mapping at the top level")

        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "PyYAML is required to save YAML files. Install with 'pip install pyyaml'.") from e

        directory = os.path.dirname(os.path.abspath(yaml_path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        data = self.to_dict()
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True)
