from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path
import os
import json
import fnmatch
import copy


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    enable_learning: bool = True
    learn_fields_include: Optional[List[str]] = None
    learn_fields_exclude: Optional[List[str]] = None
    learn_contexts_include: Optional[List[str]] = None
    learn_contexts_exclude: Optional[List[str]] = None
    default_environment: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        """Create configuration from environment variables"""
        # Allow loading from file via env var
        file_env = os.getenv('SMART_DEFAULTS_CONFIG_FILE') or os.getenv(
            'SMART_DEFAULTS_CONFIG_PATH')
        if file_env:
            path = Path(file_env)
            if path.exists():
                return cls.from_file(path)

        def _parse_bool(val: Optional[str], default: bool) -> bool:
            if val is None:
                return default
            v = val.strip().lower()
            return v in ('1', 'true', 'yes', 'on', 'y', 't')

        def _parse_list(val: Optional[str]) -> Optional[List[str]]:
            if val is None or val.strip() == '':
                return None
            s = val.strip()
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x) for x in parsed]
            except Exception:
                pass
            # Fallback to comma-separated
            return [item.strip() for item in s.split(',') if item.strip() != '']

        def _parse_environments(val: Optional[str]) -> Dict[str, Dict[str, Any]]:
            if not val:
                return {}
            try:
                parsed = json.loads(val)
                if isinstance(parsed, dict):
                    out: Dict[str, Dict[str, Any]] = {}
                    for k, v in parsed.items():
                        out[str(k)] = dict(v) if isinstance(v, dict) else {}
                    return out
            except Exception:
                return {}
            return {}

        environments = _parse_environments(
            os.getenv('SMART_DEFAULTS_ENVIRONMENTS'))
        enable_learning = _parse_bool(
            os.getenv('SMART_DEFAULTS_ENABLE_LEARNING'), True)
        learn_fields_include = _parse_list(
            os.getenv('SMART_DEFAULTS_LEARN_FIELDS_INCLUDE'))
        learn_fields_exclude = _parse_list(
            os.getenv('SMART_DEFAULTS_LEARN_FIELDS_EXCLUDE'))
        learn_contexts_include = _parse_list(
            os.getenv('SMART_DEFAULTS_LEARN_CONTEXTS_INCLUDE'))
        learn_contexts_exclude = _parse_list(
            os.getenv('SMART_DEFAULTS_LEARN_CONTEXTS_EXCLUDE'))
        default_environment = os.getenv('SMART_DEFAULTS_DEFAULT_ENV') or os.getenv(
            'SMART_DEFAULTS_DEFAULT_ENVIRONMENT')

        return cls(
            environments=environments,
            enable_learning=enable_learning,
            learn_fields_include=learn_fields_include,
            learn_fields_exclude=learn_fields_exclude,
            learn_contexts_include=learn_contexts_include,
            learn_contexts_exclude=learn_contexts_exclude,
            default_environment=default_environment or None,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        """Load configuration from JSON file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Configuration file must contain a JSON object")

        environments = data.get('environments') or {}
        if not isinstance(environments, dict):
            environments = {}

        def _as_list(key: str) -> Optional[List[str]]:
            v = data.get(key, None)
            if v is None:
                return None
            if isinstance(v, list):
                return [str(x) for x in v]
            # Accept comma-separated string
            if isinstance(v, str):
                vs = [s.strip() for s in v.split(',') if s.strip()]
                return vs or None
            return None

        enable_learning = bool(
            data.get('enable_learning', data.get('enableLearning', True)))
        learn_fields_include = _as_list(
            'learn_fields_include') or _as_list('learnFieldsInclude')
        learn_fields_exclude = _as_list(
            'learn_fields_exclude') or _as_list('learnFieldsExclude')
        learn_contexts_include = _as_list(
            'learn_contexts_include') or _as_list('learnContextsInclude')
        learn_contexts_exclude = _as_list(
            'learn_contexts_exclude') or _as_list('learnContextsExclude')
        default_environment = data.get('default_environment') or data.get(
            'defaultEnvironment') or None

        # Normalize environments to dict[str, dict]
        norm_envs: Dict[str, Dict[str, Any]] = {}
        for k, v in environments.items():
            norm_envs[str(k)] = dict(v) if isinstance(v, dict) else {}

        return cls(
            environments=norm_envs,
            enable_learning=enable_learning,
            learn_fields_include=learn_fields_include,
            learn_fields_exclude=learn_fields_exclude,
            learn_contexts_include=learn_contexts_include,
            learn_contexts_exclude=learn_contexts_exclude,
            default_environment=default_environment,
        )

    def to_file(self, config_path: Path):
        """Save configuration to JSON file"""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'environments': self.environments,
            'enable_learning': self.enable_learning,
            'learn_fields_include': self.learn_fields_include,
            'learn_fields_exclude': self.learn_fields_exclude,
            'learn_contexts_include': self.learn_contexts_include,
            'learn_contexts_exclude': self.learn_contexts_exclude,
            'default_environment': self.default_environment,
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues: List[str] = []

        if not isinstance(self.environments, dict):
            issues.append(
                "environments must be a dictionary of environment names to defaults")
        else:
            for name, defaults in self.environments.items():
                if not isinstance(name, str):
                    issues.append(f"environment key {name!r} is not a string")
                if not isinstance(defaults, dict):
                    issues.append(
                        f"defaults for environment '{name}' must be an object/dict")

        if self.default_environment and self.default_environment not in self.environments:
            issues.append(
                f"default_environment '{self.default_environment}' is not present in environments")

        def _validate_list(lst: Optional[List[str]], label: str):
            if lst is None:
                return
            if not isinstance(lst, list):
                issues.append(f"{label} must be a list of strings or null")
                return
            for i, v in enumerate(lst):
                if not isinstance(v, str):
                    issues.append(f"{label}[{i}] must be a string")

        _validate_list(self.learn_fields_include, "learn_fields_include")
        _validate_list(self.learn_fields_exclude, "learn_fields_exclude")
        _validate_list(self.learn_contexts_include, "learn_contexts_include")
        _validate_list(self.learn_contexts_exclude, "learn_contexts_exclude")

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment"""
        if environment in self.environments:
            return copy.deepcopy(self.environments[environment])
        if self.default_environment and self.default_environment in self.environments:
            return copy.deepcopy(self.environments[self.default_environment])
        if 'default' in self.environments:
            return copy.deepcopy(self.environments['default'])
        return {}

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field"""
        if not self.enable_learning:
            return False
        return self._should_learn_by_patterns(
            name=field_name,
            includes=self.learn_fields_include,
            excludes=self.learn_fields_exclude,
        )

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context"""
        if not self.enable_learning:
            return False
        return self._should_learn_by_patterns(
            name=context,
            includes=self.learn_contexts_include,
            excludes=self.learn_contexts_exclude,
        )

    @staticmethod
    def _should_learn_by_patterns(name: str, includes: Optional[List[str]], excludes: Optional[List[str]]) -> bool:
        # If includes provided, must match at least one
        if includes:
            included = any(fnmatch.fnmatch(name, pat) for pat in includes)
            if not included:
                return False
        # If excludes provided, must not match any
        if excludes:
            if any(fnmatch.fnmatch(name, pat) for pat in excludes):
                return False
        return True
