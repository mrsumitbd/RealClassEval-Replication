from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import fnmatch
import json
import os
import copy


def _parse_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    value = value.strip().lower()
    if value in ('1', 'true', 't', 'yes', 'y', 'on'):
        return True
    if value in ('0', 'false', 'f', 'no', 'n', 'off'):
        return False
    return default


def _parse_list_env(value: Optional[str]) -> Set[str]:
    if not value:
        return set()
    return {part.strip() for part in value.split(',') if part.strip()}


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    global_defaults: Dict[str, Any] = field(default_factory=dict)
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    default_environment: Optional[str] = None

    learning_enabled: bool = True
    learn_fields_include: Set[str] = field(default_factory=set)
    learn_fields_exclude: Set[str] = field(default_factory=set)
    learn_context_include: Set[str] = field(default_factory=set)
    learn_context_exclude: Set[str] = field(default_factory=set)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        # Start with file-based config if provided
        base = cls()
        file_env = os.environ.get('SMART_DEFAULTS_FILE')
        if file_env:
            try:
                base = cls.from_file(Path(file_env))
            except Exception:
                base = cls()

        # Merge/override with env variables if present
        # Global defaults JSON
        global_defaults_env = os.environ.get('SMART_DEFAULTS_GLOBAL_DEFAULTS')
        if global_defaults_env:
            try:
                base.global_defaults = json.loads(global_defaults_env)
            except Exception:
                pass

        # Environments JSON
        environments_env = os.environ.get('SMART_DEFAULTS_ENVIRONMENTS')
        if environments_env:
            try:
                envs = json.loads(environments_env)
                if isinstance(envs, dict):
                    # Ensure each value is a dict
                    cleaned: Dict[str, Dict[str, Any]] = {}
                    for k, v in envs.items():
                        if isinstance(v, dict):
                            cleaned[str(k)] = dict(v)
                    base.environments = cleaned
            except Exception:
                pass

        # Default environment
        default_env = os.environ.get('SMART_DEFAULTS_DEFAULT_ENV')
        if default_env:
            base.default_environment = default_env.strip() or None

        # Learning enabled
        learning_enabled = os.environ.get('SMART_DEFAULTS_LEARNING_ENABLED')
        if learning_enabled is not None:
            base.learning_enabled = _parse_bool(
                learning_enabled, base.learning_enabled)

        # Include/exclude lists
        fields_include = os.environ.get('SMART_DEFAULTS_LEARN_FIELDS_INCLUDE')
        if fields_include is not None:
            base.learn_fields_include = _parse_list_env(fields_include)

        fields_exclude = os.environ.get('SMART_DEFAULTS_LEARN_FIELDS_EXCLUDE')
        if fields_exclude is not None:
            base.learn_fields_exclude = _parse_list_env(fields_exclude)

        context_include = os.environ.get(
            'SMART_DEFAULTS_LEARN_CONTEXT_INCLUDE')
        if context_include is not None:
            base.learn_context_include = _parse_list_env(context_include)

        context_exclude = os.environ.get(
            'SMART_DEFAULTS_LEARN_CONTEXT_EXCLUDE')
        if context_exclude is not None:
            base.learn_context_exclude = _parse_list_env(context_exclude)

        return base

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with Path(config_path).expanduser().resolve().open('r', encoding='utf-8') as f:
            data = json.load(f)

        global_defaults = data.get(
            'global_defaults') or data.get('globalDefaults') or {}
        environments = data.get('environments') or {}
        default_environment = data.get(
            'default_environment') or data.get('defaultEnvironment')

        learning_enabled = data.get(
            'learning_enabled', data.get('learningEnabled', True))

        def _to_set(key_a: str, key_b: str) -> Set[str]:
            v = data.get(key_a, data.get(key_b, []))
            if isinstance(v, set):
                return set(v)
            if isinstance(v, list):
                return {str(x) for x in v}
            if isinstance(v, str):
                return _parse_list_env(v)
            return set()

        learn_fields_include = _to_set(
            'learn_fields_include', 'learnFieldsInclude')
        learn_fields_exclude = _to_set(
            'learn_fields_exclude', 'learnFieldsExclude')
        learn_context_include = _to_set(
            'learn_context_include', 'learnContextInclude')
        learn_context_exclude = _to_set(
            'learn_context_exclude', 'learnContextExclude')

        return cls(
            global_defaults=dict(global_defaults) if isinstance(
                global_defaults, dict) else {},
            environments={str(k): dict(v) for k, v in environments.items()} if isinstance(
                environments, dict) else {},
            default_environment=str(
                default_environment) if default_environment is not None else None,
            learning_enabled=bool(learning_enabled),
            learn_fields_include=learn_fields_include,
            learn_fields_exclude=learn_fields_exclude,
            learn_context_include=learn_context_include,
            learn_context_exclude=learn_context_exclude,
        )

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        payload = {
            'global_defaults': self.global_defaults,
            'environments': self.environments,
            'default_environment': self.default_environment,
            'learning_enabled': self.learning_enabled,
            'learn_fields_include': sorted(self.learn_fields_include),
            'learn_fields_exclude': sorted(self.learn_fields_exclude),
            'learn_context_include': sorted(self.learn_context_include),
            'learn_context_exclude': sorted(self.learn_context_exclude),
        }
        p = Path(config_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues: List[str] = []

        if not isinstance(self.global_defaults, dict):
            issues.append('global_defaults must be a dictionary')

        if not isinstance(self.environments, dict):
            issues.append('environments must be a dictionary')

        # Ensure each environment mapping is a dict
        for env, defaults in (self.environments or {}).items():
            if not isinstance(defaults, dict):
                issues.append(
                    f'environment "{env}" must map to a dictionary of defaults')

        if self.default_environment is not None:
            if self.default_environment not in self.environments:
                issues.append(
                    f'default_environment "{self.default_environment}" does not exist in environments')

        # Learning lists must be sets of strings
        for name, value in [
            ('learn_fields_include', self.learn_fields_include),
            ('learn_fields_exclude', self.learn_fields_exclude),
            ('learn_context_include', self.learn_context_include),
            ('learn_context_exclude', self.learn_context_exclude),
        ]:
            if not isinstance(value, set):
                issues.append(f'{name} must be a set of strings')
            elif not all(isinstance(x, str) for x in value):
                issues.append(f'{name} must only contain strings')

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        env_name = environment or self.default_environment
        result = copy.deepcopy(self.global_defaults or {})
        if env_name and env_name in self.environments:
            env_defaults = self.environments.get(env_name, {})
            if isinstance(env_defaults, dict):
                result.update(copy.deepcopy(env_defaults))
        return result

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        if not self.learning_enabled:
            return False

        def matches(name: str, patterns: Set[str]) -> bool:
            return any(fnmatch.fnmatch(name, pat) for pat in patterns)

        if self.learn_fields_include:
            return matches(field_name, self.learn_fields_include) and not matches(field_name, self.learn_fields_exclude)
        return not matches(field_name, self.learn_fields_exclude)

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        if not self.learning_enabled:
            return False

        def matches(name: str, patterns: Set[str]) -> bool:
            return any(fnmatch.fnmatch(name, pat) for pat in patterns)

        if self.learn_context_include:
            return matches(context, self.learn_context_include) and not matches(context, self.learn_context_exclude)
        return not matches(context, self.learn_context_exclude)
