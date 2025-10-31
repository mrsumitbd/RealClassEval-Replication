
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""
    environments: Dict[str, Dict[str, Any]] = None
    learn_from_fields: List[str] = None
    learn_from_contexts: List[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        """Create configuration from environment variables"""
        # Assuming environment variables are prefixed with 'SMART_DEFAULTS_'
        import os
        config = {}
        for key, value in os.environ.items():
            if key.startswith('SMART_DEFAULTS_'):
                config[key[len('SMART_DEFAULTS_'):].lower()] = value
        return cls.from_dict(config)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)

    def to_file(self, config_path: Path):
        """Save configuration to JSON file"""
        config_dict = asdict(self)
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SmartDefaultsConfig':
        return cls(
            environments=config_dict.get('environments', {}),
            learn_from_fields=config_dict.get('learn_from_fields', []),
            learn_from_contexts=config_dict.get('learn_from_contexts', []),
        )

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        if not self.environments:
            issues.append('Environments are not defined')
        if not self.learn_from_fields:
            issues.append('Learn from fields are not defined')
        if not self.learn_from_contexts:
            issues.append('Learn from contexts are not defined')
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment"""
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field"""
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context"""
        return context in self.learn_from_contexts
