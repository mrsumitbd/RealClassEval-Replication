
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import os
import json


@dataclass
class SmartDefaultsConfig:

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        config_data = {}
        for key, value in os.environ.items():
            if key.startswith('SMART_DEFAULTS_'):
                config_data[key[len('SMART_DEFAULTS_'):].lower()] = value
        return cls(**config_data)

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        config_data = self.__dict__
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def validate(self) -> List[str]:
        errors = []
        if not hasattr(self, 'environments'):
            errors.append("Missing 'environments' field in config.")
        if not hasattr(self, 'learning_fields'):
            errors.append("Missing 'learning_fields' field in config.")
        if not hasattr(self, 'learning_contexts'):
            errors.append("Missing 'learning_contexts' field in config.")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        if not hasattr(self, 'environments'):
            return {}
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        if not hasattr(self, 'learning_fields'):
            return False
        return field_name in self.learning_fields

    def should_learn_from_context(self, context: str) -> bool:
        if not hasattr(self, 'learning_contexts'):
            return False
        return context in self.learning_contexts
