
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any
import json


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    enabled: bool = True
    learning_rate: float = 0.1
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    field_blacklist: List[str] = field(default_factory=list)
    context_blacklist: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        import os
        config = cls()
        config.enabled = os.getenv(
            'SMART_DEFAULTS_ENABLED', 'true').lower() == 'true'
        config.learning_rate = float(
            os.getenv('SMART_DEFAULTS_LEARNING_RATE', '0.1'))
        return config

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, 'r') as f:
            data = json.load(f)
        return cls(**data)

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues = []
        if not isinstance(self.enabled, bool):
            issues.append("'enabled' must be a boolean")
        if not isinstance(self.learning_rate, (int, float)) or not 0 <= self.learning_rate <= 1:
            issues.append("'learning_rate' must be a number between 0 and 1")
        if not isinstance(self.environments, dict):
            issues.append("'environments' must be a dictionary")
        if not isinstance(self.field_blacklist, list):
            issues.append("'field_blacklist' must be a list")
        if not isinstance(self.context_blacklist, list):
            issues.append("'context_blacklist' must be a list")
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return field_name not in self.field_blacklist

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return context not in self.context_blacklist
