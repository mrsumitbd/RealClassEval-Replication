from dataclasses import dataclass, field, fields as dataclass_fields
from typing import Any, Dict, Optional, Set
from pathlib import Path


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""
    model_name: Optional[str] = None
    device: str = "auto"
    batch_size: int = 1
    # e.g., 'fp32', 'fp16', 'bf16', 'int8', 'auto'
    precision: Optional[str] = None
    num_workers: int = 0
    seed: Optional[int] = None
    max_length: Optional[int] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    beam_size: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and adjust configuration after initialization."""
        # Normalize device
        valid_devices = {"cpu", "cuda", "gpu", "mps", "auto"}
        if self.device not in valid_devices:
            raise ValueError(
                f"Invalid device '{self.device}'. Valid options: {sorted(valid_devices)}")

        if self.device == "gpu":
            self.device = "cuda"

        if self.device == "auto":
            resolved = "cpu"
            try:
                import torch  # type: ignore
                if hasattr(torch, "cuda") and torch.cuda.is_available():
                    resolved = "cuda"
                elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    resolved = "mps"
            except Exception:
                resolved = "cpu"
            self.device = resolved

        # Validate batch_size and num_workers
        if not isinstance(self.batch_size, int) or self.batch_size < 1:
            raise ValueError("batch_size must be a positive integer.")
        if not isinstance(self.num_workers, int) or self.num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer.")

        # Validate precision
        if self.precision is not None:
            valid_precisions: Set[str] = {
                "fp32", "fp16", "bf16", "int8", "auto"}
            if self.precision not in valid_precisions:
                raise ValueError(
                    f"Invalid precision '{self.precision}'. Valid options: {sorted(valid_precisions)}")

        # Validate optional numeric fields
        for name, value, check in (
            ("seed", self.seed, lambda v: isinstance(v, int)),
            ("max_length", self.max_length, lambda v: isinstance(v, int) and v > 0),
            ("temperature", self.temperature,
             lambda v: isinstance(v, (int, float)) and v >= 0),
            ("top_k", self.top_k, lambda v: isinstance(v, int) and v >= 0),
            ("top_p", self.top_p, lambda v: isinstance(
                v, (int, float)) and 0 <= v <= 1),
            ("beam_size", self.beam_size, lambda v: isinstance(v, int) and v >= 1),
        ):
            if value is not None and not check(value):
                raise ValueError(f"Invalid value for {name}: {value}")

        # Ensure extra is a dict
        if self.extra is None:
            self.extra = {}
        elif not isinstance(self.extra, dict):
            raise ValueError(
                "extra must be a dictionary of additional configuration values.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        # Collect dataclass fields except 'extra'
        known_fields = {f.name for f in dataclass_fields(
            self) if f.name != "extra"}
        result: Dict[str, Any] = {name: getattr(
            self, name) for name in known_fields}
        # Merge extras without overriding known fields
        for k, v in self.extra.items():
            if k not in result:
                result[k] = v
        return result

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        """Create a configuration instance from a dictionary."""
        if not isinstance(config_dict, dict):
            raise ValueError("config_dict must be a dictionary")

        field_names = {f.name for f in dataclass_fields(cls)}
        known: Dict[str, Any] = {}
        extra: Dict[str, Any] = {}

        for k, v in config_dict.items():
            if k in field_names and k != "extra":
                known[k] = v
            else:
                extra[k] = v

        # Pass 'extra' separately
        return cls(**known, extra=extra)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        """Load configuration from a YAML file."""
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "PyYAML is required to load YAML configurations.") from e

        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(
                f"YAML configuration file not found: {yaml_path}")

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError("YAML root must be a mapping/dictionary.")

        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        """Save configuration to a YAML file."""
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "PyYAML is required to save YAML configurations.") from e

        path = Path(yaml_path)
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=True,
                           default_flow_style=False)
