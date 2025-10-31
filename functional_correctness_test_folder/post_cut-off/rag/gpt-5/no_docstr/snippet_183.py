from dataclasses import dataclass, field
from typing import Any, Dict, ClassVar
from pathlib import Path
import copy
import yaml
import os


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and adjust configuration after initialization."""
        if self.data is None:
            self.data = {}
        if not isinstance(self.data, dict):
            raise TypeError('InferenceConfig.data must be a dict')
        normalized: Dict[str, Any] = {}
        for k, v in self.data.items():
            key = str(k)
            normalized[key] = v
        self.data = normalized

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        def _serialize(obj: Any) -> Any:
            if isinstance(obj, Path):
                return str(obj)
            if isinstance(obj, set):
                return sorted(list(obj))
            if isinstance(obj, tuple):
                return list(obj)
            if isinstance(obj, dict):
                return {str(k): _serialize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_serialize(i) for i in obj]
            try:
                # Attempt to convert dataclass-like structures
                from dataclasses import asdict, is_dataclass
                if is_dataclass(obj):
                    return _serialize(asdict(obj))
            except Exception:
                pass
            return obj

        return _serialize(copy.deepcopy(self.data))

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        """Create a configuration instance from a dictionary."""
        if config_dict is None:
            config_dict = {}
        if not isinstance(config_dict, dict):
            raise TypeError('from_dict expects a dict')
        return cls(data=copy.deepcopy(config_dict))

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        """Load configuration from a YAML file."""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f'YAML file not found: {path}')
        with path.open('r', encoding='utf-8') as f:
            content = yaml.safe_load(f) or {}
        if not isinstance(content, dict):
            raise ValueError(
                'YAML content must be a mapping at the document root')
        return cls.from_dict(content)

    def save_yaml(self, yaml_path: str) -> None:
        """Save configuration to a YAML file."""
        path = Path(yaml_path)
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=True,
                           allow_unicode=True, default_flow_style=False)

    def __getattr__(self, name: str) -> Any:
        if 'data' in self.__dict__ and name in self.data:
            return self.data[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in {'data'} or name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        d = self.__dict__.get('data')
        if isinstance(d, dict):
            d[name] = value
        else:
            object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        if name in {'data'} or name.startswith('_'):
            object.__delattr__(self, name)
            return
        d = self.__dict__.get('data')
        if isinstance(d, dict) and name in d:
            del d[name]
        else:
            object.__delattr__(self, name)
