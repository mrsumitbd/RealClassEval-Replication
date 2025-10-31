from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import json
import os


def _parse_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in ('1', 'true', 'yes', 'on'):
        return True
    if v in ('0', 'false', 'no', 'off'):
        return False
    return default


def _parse_csv_set(value: Optional[str]) -> Set[str]:
    if value is None:
        return set()
    parts = [p.strip() for p in value.split(',')]
    return {p for p in parts if p}


def _parse_json_dict(value: Optional[str]) -> Dict[str, Any]:
    if value is None:
        return {}
    try:
        obj = json.loads(value)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    enabled: bool = True
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    include_fields: Optional[Set[str]] = None
    exclude_fields: Set[str] = field(default_factory=set)
    include_contexts: Optional[Set[str]] = None
    exclude_contexts: Set[str] = field(default_factory=set)
    max_examples: int = 1000
    storage_path: Optional[str] = None
    current_environment: Optional[str] = None
    version: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        enabled = _parse_bool(os.environ.get('SMART_DEFAULTS_ENABLED'), True)

        env_map = _parse_json_dict(
            os.environ.get('SMART_DEFAULTS_ENVIRONMENTS'))

        include_fields_raw = os.environ.get('SMART_DEFAULTS_INCLUDE_FIELDS')
        include_fields = None if include_fields_raw is None else _parse_csv_set(
            include_fields_raw)
        exclude_fields = _parse_csv_set(
            os.environ.get('SMART_DEFAULTS_EXCLUDE_FIELDS'))

        include_contexts_raw = os.environ.get(
            'SMART_DEFAULTS_INCLUDE_CONTEXTS')
        include_contexts = None if include_contexts_raw is None else _parse_csv_set(
            include_contexts_raw)
        exclude_contexts = _parse_csv_set(
            os.environ.get('SMART_DEFAULTS_EXCLUDE_CONTEXTS'))

        max_examples_str = os.environ.get('SMART_DEFAULTS_MAX_EXAMPLES')
        try:
            max_examples = int(
                max_examples_str) if max_examples_str is not None else 1000
        except ValueError:
            max_examples = 1000

        storage_path = os.environ.get('SMART_DEFAULTS_STORAGE_PATH') or None

        current_environment = (
            os.environ.get('SMART_DEFAULTS_CURRENT_ENV')
            or os.environ.get('SMART_DEFAULTS_ENV')
            or None
        )

        version = os.environ.get('SMART_DEFAULTS_VERSION') or None

        return cls(
            enabled=enabled,
            environments=env_map,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            include_contexts=include_contexts,
            exclude_contexts=exclude_contexts,
            max_examples=max_examples,
            storage_path=storage_path,
            current_environment=current_environment,
            version=version,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with config_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        def to_set_opt(val) -> Optional[Set[str]]:
            if val is None:
                return None
            if isinstance(val, list):
                return set(str(x) for x in val)
            if isinstance(val, str):
                return _parse_csv_set(val)
            return None

        def to_set(val) -> Set[str]:
            if val is None:
                return set()
            if isinstance(val, list):
                return set(str(x) for x in val)
            if isinstance(val, str):
                return _parse_csv_set(val)
            return set()

        return cls(
            enabled=bool(data.get('enabled', True)),
            environments=dict(data.get('environments', {})),
            include_fields=to_set_opt(data.get('include_fields')),
            exclude_fields=to_set(data.get('exclude_fields')),
            include_contexts=to_set_opt(data.get('include_contexts')),
            exclude_contexts=to_set(data.get('exclude_contexts')),
            max_examples=int(data.get('max_examples', 1000)),
            storage_path=(data.get('storage_path') or None),
            current_environment=(data.get('current_environment') or None),
            version=(data.get('version') or None),
        )

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'enabled': self.enabled,
            'environments': self.environments,
            'include_fields': sorted(list(self.include_fields)) if self.include_fields is not None else None,
            'exclude_fields': sorted(list(self.exclude_fields)),
            'include_contexts': sorted(list(self.include_contexts)) if self.include_contexts is not None else None,
            'exclude_contexts': sorted(list(self.exclude_contexts)),
            'max_examples': self.max_examples,
            'storage_path': self.storage_path,
            'current_environment': self.current_environment,
            'version': self.version,
        }
        with config_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues: List[str] = []

        if not isinstance(self.enabled, bool):
            issues.append('enabled must be a boolean')

        if not isinstance(self.max_examples, int) or self.max_examples < 0:
            issues.append('max_examples must be a non-negative integer')

        if not isinstance(self.environments, dict):
            issues.append(
                'environments must be a dictionary of environment -> defaults')
        else:
            for k, v in self.environments.items():
                if not isinstance(k, str):
                    issues.append('environment key must be a string')
                if not isinstance(v, dict):
                    issues.append(
                        f'environment "{k}" defaults must be a dictionary')

        if self.include_fields is not None:
            if not isinstance(self.include_fields, set):
                issues.append('include_fields must be a set or null')
            overlap = self.exclude_fields & self.include_fields
            if overlap:
                issues.append(
                    f'fields present in both include_fields and exclude_fields: {sorted(list(overlap))}')

        if not isinstance(self.exclude_fields, set):
            issues.append('exclude_fields must be a set')

        if self.include_contexts is not None:
            if not isinstance(self.include_contexts, set):
                issues.append('include_contexts must be a set or null')
            overlap = self.exclude_contexts & self.include_contexts
            if overlap:
                issues.append(
                    f'contexts present in both include_contexts and exclude_contexts: {sorted(list(overlap))}')

        if not isinstance(self.exclude_contexts, set):
            issues.append('exclude_contexts must be a set')

        if self.current_environment and self.current_environment not in self.environments and 'default' not in self.environments:
            issues.append(
                f'current_environment "{self.current_environment}" not found in environments and no "default" provided')

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        if not isinstance(self.environments, dict):
            return {}
        if environment in self.environments:
            return dict(self.environments[environment])
        # Fallback to case-insensitive match
        lower_map = {k.lower(): k for k in self.environments.keys()}
        key = lower_map.get(environment.lower())
        if key:
            return dict(self.environments[key])
        # Fallback to "default"
        if 'default' in self.environments:
            return dict(self.environments['default'])
        return {}

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        if not self.enabled:
            return False
        allowed = True
        if self.include_fields is not None:
            allowed = field_name in self.include_fields
        if field_name in self.exclude_fields:
            allowed = False
        return allowed

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        if not self.enabled:
            return False
        allowed = True
        if self.include_contexts is not None:
            allowed = context in self.include_contexts
        if context in self.exclude_contexts:
            allowed = False
        return allowed
