from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional
import os
import yaml


@dataclass
class InferenceConfig:
    '''Configuration for inference runs.'''
    model_name: str = "default"
    device: str = "auto"  # "cpu", "cuda", "mps", or "auto"
    batch_size: int = 1
    precision: str = "fp16"  # "fp32", "fp16", "bf16", "int8"
    num_threads: Optional[int] = None
    seed: Optional[int] = None
    max_seq_len: Optional[int] = None
    temperature: float = 0.0
    top_k: int = 50
    top_p: float = 1.0
    repetition_penalty: float = 1.0
    extras: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Validate and adjust configuration after initialization.'''
        # Normalize precision
        allowed_precisions = {"fp32", "fp16", "bf16", "int8"}
        self.precision = str(self.precision).lower()
        if self.precision not in allowed_precisions:
            self.precision = "fp16"

        # Normalize device
        self.device = str(self.device).lower()
        if self.device == "auto":
            resolved = "cpu"
            try:
                import torch  # type: ignore
                if hasattr(torch, "cuda") and torch.cuda.is_available():
                    resolved = "cuda"
                elif hasattr(torch.backends, "mps") and getattr(torch.backends.mps, "is_available", lambda: False)():
                    resolved = "mps"
            except Exception:
                resolved = "cpu"
            self.device = resolved
        elif self.device not in {"cpu", "cuda", "mps"}:
            self.device = "cpu"

        # Validate integers
        def _as_int(value, default=None):
            if value is None:
                return default
            try:
                iv = int(value)
                return iv
            except Exception:
                return default

        self.batch_size = max(1, _as_int(self.batch_size, 1))
        self.num_threads = _as_int(self.num_threads, None)
        if self.num_threads is not None and self.num_threads <= 0:
            self.num_threads = None

        self.seed = _as_int(self.seed, None)
        self.max_seq_len = _as_int(self.max_seq_len, None)
        if self.max_seq_len is not None and self.max_seq_len <= 0:
            self.max_seq_len = None

        # Validate floats
        def _as_float(value, default):
            try:
                return float(value)
            except Exception:
                return default

        self.temperature = max(0.0, _as_float(self.temperature, 0.0))
        self.top_p = _as_float(self.top_p, 1.0)
        if not (0.0 < self.top_p <= 1.0):
            self.top_p = 1.0

        self.top_k = max(0, _as_int(self.top_k, 50))
        self.repetition_penalty = _as_float(self.repetition_penalty, 1.0)
        if self.repetition_penalty <= 0.0:
            self.repetition_penalty = 1.0

        # Ensure extras is a dict
        if not isinstance(self.extras, dict):
            self.extras = {}

    def to_dict(self) -> Dict[str, Any]:
        base = asdict(self)
        extras = base.pop("extras", {}) or {}
        merged = {**extras, **base}
        return merged

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        '''Create a configuration instance from a dictionary.'''
        if not isinstance(config_dict, dict):
            raise TypeError("config_dict must be a dictionary")
        # type: ignore
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        known = {}
        extras = {}
        for k, v in config_dict.items():
            if k in field_names and k != "extras":
                known[k] = v
            else:
                extras[k] = v
        return cls(**known, extras=extras)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        '''Load configuration from a YAML file.'''
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError("YAML content must be a mapping")
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        '''Save configuration to a YAML file.'''
        os.makedirs(os.path.dirname(os.path.abspath(yaml_path)), exist_ok=True)
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=True,
                           allow_unicode=True)
