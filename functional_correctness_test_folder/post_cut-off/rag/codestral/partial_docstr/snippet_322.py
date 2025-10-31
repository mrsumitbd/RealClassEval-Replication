
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import os


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learning_enabled: bool = True
    learning_fields: List[str] = field(default_factory=list)
    learning_contexts: List[str] = field(default_factory=list)
    default_environment: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        config = cls()
        config.learning_enabled = os.getenv(
            'SMART_DEFAULTS_LEARNING_ENABLED', 'true').lower() == 'true'
        config.default_environment = os.getenv(
            'SMART_DEFAULTS_DEFAULT_ENVIRONMENT')
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
        if not self.environments:
            issues.append("No environments configured")
        if self.default_environment and self.default_environment not in self.environments:
            issues.append(
                f"Default environment '{self.default_environment}' not found in configured environments")
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        if environment not in self.environments:
            raise ValueError(f"Environment '{environment}' not found")
        return self.environments[environment]

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return self.learning_enabled and (not self.learning_fields or field_name in self.learning_fields)

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return self.learning_enabled and (not self.learning_contexts or context in self.learning_contexts)
