from pathlib import Path
from typing import Optional, Dict, Any
import json
import dataclasses
from enum import Enum


class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize with config directory."""
        if config_dir is None:
            config_dir = Path.cwd()
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._file = self.config_dir / 'last_used.json'

    def save(self, settings: 'Settings') -> None:
        """Save current settings as last used."""
        data = self._settings_to_dict(settings)
        data = self._to_jsonable(data)
        tmp_file = self._file.with_suffix(self._file.suffix + '.tmp')
        with tmp_file.open('w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        tmp_file.replace(self._file)

    def load(self) -> Dict[str, Any]:
        """Load last used parameters."""
        if not self._file.exists():
            return {}
        try:
            with self._file.open('r', encoding='utf-8') as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}

    def clear(self) -> None:
        """Clear last used parameters."""
        try:
            if self._file.exists():
                self._file.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        """Check if last used params exist."""
        return self._file.exists()

    @staticmethod
    def _settings_to_dict(settings: Any) -> Dict[str, Any]:
        if hasattr(settings, 'to_dict') and callable(getattr(settings, 'to_dict')):
            result = settings.to_dict()
            if isinstance(result, dict):
                return result
        if dataclasses.is_dataclass(settings):
            return dataclasses.asdict(settings)
        if hasattr(settings, '__dict__') and isinstance(settings.__dict__, dict):
            return {k: v for k, v in settings.__dict__.items() if not k.startswith('_')}
        if isinstance(settings, dict):
            return settings
        raise TypeError('Unsupported settings object for serialization')

    @classmethod
    def _to_jsonable(cls, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', errors='replace')
            except Exception:
                return str(value)
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, dict):
            return {str(k): cls._to_jsonable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [cls._to_jsonable(v) for v in value]
        if dataclasses.is_dataclass(value):
            return cls._to_jsonable(dataclasses.asdict(value))
        if hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
            try:
                return cls._to_jsonable(value.to_dict())
            except Exception:
                return str(value)
        if hasattr(value, '__dict__'):
            try:
                return cls._to_jsonable({k: v for k, v in value.__dict__.items() if not k.startswith('_')})
            except Exception:
                return str(value)
        return str(value)
