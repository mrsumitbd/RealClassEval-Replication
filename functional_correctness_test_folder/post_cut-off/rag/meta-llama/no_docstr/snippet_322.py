
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
        # Assuming environment variables are prefixed with SMART_DEFAULTS_
        # and are in the format SMART_DEFAULTS_ENVIRONMENTS_dev_key=value
        # and SMART_DEFAULTS_LEARN_FROM_FIELDS=field1,field2
        # and SMART_DEFAULTS_LEARN_FROM_CONTEXTS=context1,context2
        environments = {}
        learn_from_fields = []
        learn_from_contexts = []
        import os
        for key, value in os.environ.items():
            if key.startswith('SMART_DEFAULTS_'):
                if key.startswith('SMART_DEFAULTS_ENVIRONMENTS_'):
                    env_name = key.split('_')[2]
                    env_key = '_'.join(key.split('_')[3:])
                    if env_name not in environments:
                        environments[env_name] = {}
                    environments[env_name][env_key] = value
                elif key == 'SMART_DEFAULTS_LEARN_FROM_FIELDS':
                    learn_from_fields = value.split(',')
                elif key == 'SMART_DEFAULTS_LEARN_FROM_CONTEXTS':
                    learn_from_contexts = value.split(',')
        return cls(environments=environments, learn_from_fields=learn_from_fields, learn_from_contexts=learn_from_contexts)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        return cls(**config_dict)

    def to_file(self, config_path: Path):
        """Save configuration to JSON file"""
        config_dict = asdict(self)
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        if not self.environments:
            issues.append('No environments defined')
        if not self.learn_from_fields:
            issues.append('No fields to learn from defined')
        if not self.learn_from_contexts:
            issues.append('No contexts to learn from defined')
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
