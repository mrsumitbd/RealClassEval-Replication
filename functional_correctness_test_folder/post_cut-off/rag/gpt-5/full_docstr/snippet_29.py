from pathlib import Path
from typing import Optional, Dict, Any, Mapping
import json
import os
import dataclasses
import tempfile


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            # Fallback to a generic per-user config directory
            config_dir = Path.home() / '.config' / 'last_used_params'
        self.config_dir: Path = Path(config_dir)
        self.path: Path = self.config_dir / 'last_used.json'

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        try:
            data = self._settings_to_dict(settings)
        except Exception:
            # If settings cannot be converted to dict, do nothing
            return

        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False, dir=str(self.config_dir)) as tmp:
                json.dump(data, tmp, ensure_ascii=False,
                          indent=2, sort_keys=True)
                tmp.flush()
                os.fsync(tmp.fileno())
                tmp_name = tmp.name
            os.replace(tmp_name, self.path)
        except Exception:
            # Best-effort persistence; ignore failures
            try:
                if 'tmp_name' in locals() and os.path.exists(tmp_name):
                    os.unlink(tmp_name)
            except Exception:
                pass

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        try:
            with self.path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        try:
            if self.path.exists():
                self.path.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.path.exists()

    @staticmethod
    def _settings_to_dict(settings: Any) -> Dict[str, Any]:
        # Prefer explicit conversions if available
        for attr in ('to_last_used', 'last_used', 'to_dict', 'dict'):
            fn = getattr(settings, attr, None)
            if callable(fn):
                result = fn()
                if isinstance(result, Mapping):
                    return dict(result)
        # Dataclass support
        if dataclasses.is_dataclass(settings):
            return dataclasses.asdict(settings)
        # Mapping-like
        if isinstance(settings, Mapping):
            return dict(settings)
        # Fallback to object __dict__
        if hasattr(settings, '__dict__'):
            return dict(vars(settings))
        # If all else fails, raise to be caught by caller
        raise TypeError('Settings object is not serializable to dict')
