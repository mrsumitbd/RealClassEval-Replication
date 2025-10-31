
from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path
import json
import os


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learnable_fields: List[str] = field(default_factory=list)
    learnable_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        environments = json.loads(
            os.getenv('SMART_DEFAULTS_ENVIRONMENTS', '{}'))
        learnable_fields = os.getenv(
            'SMART_DEFAULTS_LEARNABLE_FIELDS', '').split(',')
        learnable_contexts = os.getenv(
            'SMART_DEFAULTS_LEARNABLE_CONTEXTS', '').split(',')
        return cls(environments=environments, learnable_fields=learnable_fields, learnable_contexts=learnable_contexts)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, 'r') as file:
            data = json.load(file)
        return cls(**data)

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        with open(config_path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues = []
        if not isinstance(self.environments, dict):
            issues.append("Environments should be a dictionary.")
        if not all(isinstance(env, dict) for env in self.environments.values()):
            issues.append("Each environment should be a dictionary.")
        if not isinstance(self.learnable_fields, list):
            issues.append("Learnable fields should be a list.")
        if not isinstance(self.learnable_contexts, list):
            issues.append("Learnable contexts should be a list.")
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return field_name in self.learnable_fields

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return context in self.learnable_contexts
