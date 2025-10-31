from __future__ import annotations

from dataclasses import dataclass, fields, asdict, is_dataclass, Field
from typing import Any, Dict, Type, get_type_hints, get_origin, get_args
from pathlib import Path
import os
import enum


@dataclass
class InferenceConfig:
    """Configuration for inference runs."""

    def __post_init__(self):
        """Validate and adjust configuration after initialization."""
        type_hints = get_type_hints(type(self))
        for f in fields(self):
            if not f.init:
                continue
            name = f.name
            if name.startswith('_'):
                continue
            if name not in type_hints:
                continue
            target_type = type_hints[name]
            value = getattr(self, name)
            coerced = self._coerce_value(target_type, value)
            setattr(self, name, coerced)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        raw = asdict(self)
        # Drop private fields and serialize complex types
        result: Dict[str, Any] = {}
        for k, v in raw.items():
            if k.startswith('_'):
                continue
            result[k] = self._serialize_value(v)
        return result

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'InferenceConfig':
        """Create a configuration instance from a dictionary."""
        if not isinstance(config_dict, dict):
            raise TypeError('config_dict must be a dict')
        type_hints = get_type_hints(cls)
        init_field_names = {f.name for f in fields(cls) if f.init}
        kwargs: Dict[str, Any] = {}
        for k in init_field_names:
            if k in config_dict:
                target_type = type_hints.get(k)
                value = config_dict[k]
                if target_type is not None:
                    value = cls._coerce_value(target_type, value)
                kwargs[k] = value
        return cls(**kwargs)  # type: ignore[arg-type]

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'InferenceConfig':
        """Load configuration from a YAML file."""
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise ImportError('PyYAML is required to use from_yaml') from e

        path = Path(os.path.expandvars(os.path.expanduser(yaml_path)))
        if not path.exists():
            raise FileNotFoundError(f'YAML file not found: {path}')
        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError('YAML content must be a mapping at the top level')
        return cls.from_dict(data)

    def save_yaml(self, yaml_path: str) -> None:
        """Save configuration to a YAML file."""
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise ImportError('PyYAML is required to use save_yaml') from e

        path = Path(os.path.expandvars(os.path.expanduser(yaml_path)))
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        data = self.to_dict()
        with path.open('w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, enum.Enum):
            return value.value
        if is_dataclass(value):
            return {k: InferenceConfig._serialize_value(v) for k, v in asdict(value).items()}
        if isinstance(value, dict):
            return {k: InferenceConfig._serialize_value(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [InferenceConfig._serialize_value(v) for v in value]
        return value

    @staticmethod
    def _coerce_value(target_type: Type[Any], value: Any) -> Any:
        origin = get_origin(target_type)
        args = get_args(target_type)

        # Handle Optional/Union
        if origin is None and hasattr(target_type, '__args__'):
            origin = get_origin(target_type)
            args = get_args(target_type)

        if origin is None:
            # Simple types and special handling
            try:
                if target_type is Path:
                    if value is None:
                        return None
                    if isinstance(value, Path):
                        return value.expanduser().resolve(strict=False)
                    return Path(os.path.expandvars(os.path.expanduser(str(value)))).resolve(strict=False)
                if isinstance(target_type, type) and issubclass(target_type, enum.Enum):
                    if isinstance(value, target_type):
                        return value
                    # Try match by value then by name
                    for member in target_type:
                        if value == member.value or str(value) == str(member.value) or str(value) == member.name:
                            return member
                    return value
                if target_type is bool:
                    if isinstance(value, bool):
                        return value
                    if isinstance(value, (int, float)):
                        return bool(value)
                    if isinstance(value, str):
                        v = value.strip().lower()
                        if v in {'1', 'true', 't', 'yes', 'y', 'on'}:
                            return True
                        if v in {'0', 'false', 'f', 'no', 'n', 'off'}:
                            return False
                    return bool(value)
                if target_type is int:
                    if isinstance(value, int):
                        return value
                    if isinstance(value, bool):
                        return int(value)
                    return int(str(value).strip())
                if target_type is float:
                    if isinstance(value, float):
                        return value
                    if isinstance(value, bool):
                        return float(int(value))
                    return float(str(value).strip())
                if target_type is str:
                    if value is None:
                        return ''
                    s = str(value)
                    # Expand env vars in strings
                    s = os.path.expandvars(os.path.expanduser(s))
                    return s
                # Fallback to direct construction if possible
                if isinstance(value, target_type):
                    return value
                try:
                    return target_type(value)  # type: ignore
                except Exception:
                    return value
            except Exception:
                return value

        # Handle Optional[T] or Union
        if origin is Union := getattr(__import__('typing'), 'Union'):
            # Try each type in Union (excluding NoneType)
            non_none_args = [a for a in args if a is not type(None)]
            if value is None:
                return None
            for a in non_none_args:
                coerced = InferenceConfig._coerce_value(a, value)
                if InferenceConfig._is_instance_of(coerced, a):
                    return coerced
            return value

        # Handle List[T], Tuple[T,...], Set[T]
        if origin in (list, tuple, set):
            elem_type = args[0] if args else Any
            if not isinstance(value, (list, tuple, set)):
                value = [value] if value is not None else []
            coerced_elems = [InferenceConfig._coerce_value(
                elem_type, v) for v in value]
            if origin is tuple:
                return tuple(coerced_elems)
            if origin is set:
                return set(coerced_elems)
            return coerced_elems

        # Handle Dict[K, V]
        if origin is dict:
            key_type = args[0] if len(args) > 0 else Any
            val_type = args[1] if len(args) > 1 else Any
            if not isinstance(value, dict):
                return value
            return {
                InferenceConfig._coerce_value(key_type, k): InferenceConfig._coerce_value(val_type, v)
                for k, v in value.items()
            }

        # Fallback
        return value

    @staticmethod
    def _is_instance_of(value: Any, type_hint: Type[Any]) -> bool:
        origin = get_origin(type_hint)
        if origin is None:
            try:
                return isinstance(value, type_hint)  # type: ignore[arg-type]
            except Exception:
                return True  # Best effort
        if origin in (list, tuple, set):
            return isinstance(value, origin)
        if origin is dict:
            return isinstance(value, dict)
        return True
