import os
import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, get_args, get_origin


@dataclass
class BiomniConfig:
    '''Central configuration for Biomni agent.
    All settings are optional and have sensible defaults.
    API keys are still read from environment variables to maintain
    compatibility with existing .env file structure.
    Usage:
        # Create config with defaults
        config = BiomniConfig()
        # Override specific settings
        config = BiomniConfig(llm="gpt-4", timeout_seconds=1200)
        # Modify after creation
        config.path = "./custom_data"
    '''

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        self._apply_biomni_prefixed_env_overrides()
        self._load_legacy_api_keys()

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        result = {}
        declared = {f.name for f in fields(self)}
        # Include declared dataclass fields
        result.update({k: self._serialize(v) for k, v in asdict(self).items()})
        # Include any dynamically added attributes (e.g., API keys)
        dynamic_attrs = {k: v for k, v in self.__dict__.items(
        ) if k not in declared and not k.startswith('_')}
        result.update({k: self._serialize(v)
                      for k, v in dynamic_attrs.items()})
        return result

    # Internal helpers

    def _apply_biomni_prefixed_env_overrides(self) -> None:
        for f in fields(self):
            env_name = f'BIOMNI_{f.name}'.upper()
            if env_name in os.environ:
                raw = os.environ[env_name]
                try:
                    setattr(self, f.name, self._coerce(raw, f.type))
                except Exception:
                    setattr(self, f.name, raw)

    def _load_legacy_api_keys(self) -> None:
        # Compatibility with common provider ENV names
        env_map = {
            'openai_api_key': ['OPENAI_API_KEY'],
            'openai_base_url': ['OPENAI_BASE_URL', 'OPENAI_API_BASE'],
            'openai_organization': ['OPENAI_ORG_ID', 'OPENAI_ORGANIZATION'],

            'anthropic_api_key': ['ANTHROPIC_API_KEY'],

            'azure_openai_api_key': ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_KEY'],
            'azure_openai_endpoint': ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_BASE_URL'],
            'azure_openai_deployment': ['AZURE_OPENAI_DEPLOYMENT', 'AZURE_OPENAI_MODEL'],
            'azure_openai_api_version': ['AZURE_OPENAI_API_VERSION'],

            'google_api_key': ['GOOGLE_API_KEY', 'GOOGLEAI_API_KEY', 'GEMINI_API_KEY'],

            'groq_api_key': ['GROQ_API_KEY'],
        }
        for attr, candidates in env_map.items():
            for name in candidates:
                if name in os.environ and os.environ[name]:
                    setattr(self, attr, os.environ[name])
                    break

    @staticmethod
    def _coerce(value: str, type_hint: Any) -> Any:
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        # Optional[T] -> T
        if origin is None and hasattr(type_hint, '__args__'):
            origin = get_origin(type_hint)
            args = get_args(type_hint)

        if origin is None:
            # Handle common primitives and Path
            if type_hint in (str, Any, None):
                return value
            if type_hint is bool:
                return value.strip().lower() in {'1', 'true', 'yes', 'on', 'y', 't'}
            if type_hint is int:
                return int(value.strip())
            if type_hint is float:
                return float(value.strip())
            if type_hint is Path:
                return Path(value)
            # Fallback
            return value

        # Optional[T]
        if origin is getattr(__import__('typing'), 'Union', None) and type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            return BiomniConfig._coerce(value, non_none[0] if non_none else Any)

        # List / Dict via JSON or simple parsing
        if origin in (list, tuple, set):
            try:
                loaded = json.loads(value)
                if not isinstance(loaded, list):
                    loaded = [loaded]
            except Exception:
                loaded = [v.strip()
                          for v in value.split(',')] if value.strip() else []
            return origin(loaded)

        if origin is dict:
            try:
                loaded = json.loads(value)
                if not isinstance(loaded, dict):
                    raise ValueError
                return loaded
            except Exception:
                # naive key=value,key2=value2 parsing
                result = {}
                for part in [p for p in value.split(',') if p.strip()]:
                    if '=' in part:
                        k, v = part.split('=', 1)
                        result[k.strip()] = v.strip()
                return result

        return value

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, (list, tuple)):
            return [BiomniConfig._serialize(v) for v in value]
        if isinstance(value, dict):
            return {k: BiomniConfig._serialize(v) for k, v in value.items()}
        return value
