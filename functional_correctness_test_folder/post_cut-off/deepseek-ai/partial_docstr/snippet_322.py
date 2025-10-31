
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import os
import json


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    defaults: Dict[str, Any]
    learning_fields: List[str]
    learning_contexts: List[str]

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        defaults = json.loads(os.getenv('SMART_DEFAULTS', '{}'))
        learning_fields = json.loads(os.getenv('LEARNING_FIELDS', '[]'))
        learning_contexts = json.loads(os.getenv('LEARNING_CONTEXTS', '[]'))
        return cls(defaults, learning_fields, learning_contexts)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, 'r') as f:
            config = json.load(f)
        return cls(
            defaults=config.get('defaults', {}),
            learning_fields=config.get('learning_fields', []),
            learning_contexts=config.get('learning_contexts', [])
        )

    def to_file(self, config_path: Path):
        config = {
            'defaults': self.defaults,
            'learning_fields': self.learning_fields,
            'learning_contexts': self.learning_contexts
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def validate(self) -> List[str]:
        errors = []
        if not isinstance(self.defaults, dict):
            errors.append("Defaults must be a dictionary")
        if not isinstance(self.learning_fields, list):
            errors.append("Learning fields must be a list")
        if not isinstance(self.learning_contexts, list):
            errors.append("Learning contexts must be a list")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.defaults.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learning_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learning_contexts
