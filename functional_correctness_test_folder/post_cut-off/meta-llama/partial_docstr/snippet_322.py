
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
import json
import os


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    learn_from_fields: List[str]
    learn_from_contexts: List[str]
    environment_defaults: Dict[str, Dict[str, Any]]

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        config_path = Path(os.environ.get(
            'SMART_DEFAULTS_CONFIG', 'config.json'))
        return cls.from_file(config_path)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        config_data = asdict(self)
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def validate(self) -> List[str]:
        errors = []
        if not self.learn_from_fields:
            errors.append('learn_from_fields is empty')
        if not self.learn_from_contexts:
            errors.append('learn_from_contexts is empty')
        if not self.environment_defaults:
            errors.append('environment_defaults is empty')
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return self.environment_defaults.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return context in self.learn_from_contexts
