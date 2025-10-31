
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    learn_from_fields: List[str]
    learn_from_contexts: List[str]
    environment_defaults: Dict[str, Dict[str, Any]]

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        import os
        learn_from_fields = os.environ.get('LEARN_FROM_FIELDS', '').split(',')
        learn_from_contexts = os.environ.get(
            'LEARN_FROM_CONTEXTS', '').split(',')
        environment_defaults = json.loads(
            os.environ.get('ENVIRONMENT_DEFAULTS', '{}'))
        return cls(
            learn_from_fields=[field.strip()
                               for field in learn_from_fields if field.strip()],
            learn_from_contexts=[
                context.strip() for context in learn_from_contexts if context.strip()],
            environment_defaults=environment_defaults
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, 'r') as file:
            config_data = json.load(file)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        with open(config_path, 'w') as file:
            json.dump(asdict(self), file, indent=4)

    def validate(self) -> List[str]:
        issues = []
        if not self.learn_from_fields:
            issues.append('No fields are configured for learning')
        if not self.learn_from_contexts:
            issues.append('No contexts are configured for learning')
        if not self.environment_defaults:
            issues.append('No environment defaults are configured')
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environment_defaults.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learn_from_contexts
