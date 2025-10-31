
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import json
import os


@dataclass
class SmartDefaultsConfig:
    environment_defaults: Dict[str, Dict[str, Any]
                               ] = field(default_factory=dict)
    learnable_fields: List[str] = field(default_factory=list)
    learnable_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        env_defaults = json.loads(os.getenv('SMART_DEFAULTS_CONFIG', '{}'))
        learnable_fields = os.getenv('SMART_LEARNABLE_FIELDS', '').split(',')
        learnable_contexts = os.getenv(
            'SMART_LEARNABLE_CONTEXTS', '').split(',')
        return cls(
            environment_defaults=env_defaults,
            learnable_fields=learnable_fields,
            learnable_contexts=learnable_contexts
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with config_path.open('r') as file:
            config_data = json.load(file)
        return cls(
            environment_defaults=config_data.get('environment_defaults', {}),
            learnable_fields=config_data.get('learnable_fields', []),
            learnable_contexts=config_data.get('learnable_contexts', [])
        )

    def to_file(self, config_path: Path):
        config_data = {
            'environment_defaults': self.environment_defaults,
            'learnable_fields': self.learnable_fields,
            'learnable_contexts': self.learnable_contexts
        }
        with config_path.open('w') as file:
            json.dump(config_data, file, indent=4)

    def validate(self) -> List[str]:
        errors = []
        if not isinstance(self.environment_defaults, dict):
            errors.append("environment_defaults must be a dictionary.")
        if not isinstance(self.learnable_fields, list):
            errors.append("learnable_fields must be a list.")
        if not isinstance(self.learnable_contexts, list):
            errors.append("learnable_contexts must be a list.")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environment_defaults.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learnable_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learnable_contexts
