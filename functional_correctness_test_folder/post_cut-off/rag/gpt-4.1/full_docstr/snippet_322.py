from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List
from pathlib import Path
import os
import json


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_from_fields: List[str] = field(default_factory=list)
    learn_from_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        envs = os.environ.get('SMART_DEFAULTS_ENVIRONMENTS')
        fields = os.environ.get('SMART_DEFAULTS_LEARN_FIELDS')
        contexts = os.environ.get('SMART_DEFAULTS_LEARN_CONTEXTS')
        environments = {}
        if envs:
            try:
                environments = json.loads(envs)
            except Exception:
                environments = {}
        learn_from_fields = fields.split(',') if fields else []
        learn_from_contexts = contexts.split(',') if contexts else []
        return cls(
            environments=environments,
            learn_from_fields=[f.strip()
                               for f in learn_from_fields if f.strip()],
            learn_from_contexts=[c.strip()
                                 for c in learn_from_contexts if c.strip()]
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(
            environments=data.get('environments', {}),
            learn_from_fields=data.get('learn_from_fields', []),
            learn_from_contexts=data.get('learn_from_contexts', [])
        )

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues = []
        if not isinstance(self.environments, dict):
            issues.append("environments must be a dictionary")
        for env, defaults in self.environments.items():
            if not isinstance(defaults, dict):
                issues.append(
                    f"Defaults for environment '{env}' must be a dictionary")
        if not isinstance(self.learn_from_fields, list):
            issues.append("learn_from_fields must be a list")
        if not isinstance(self.learn_from_contexts, list):
            issues.append("learn_from_contexts must be a list")
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return context in self.learn_from_contexts
