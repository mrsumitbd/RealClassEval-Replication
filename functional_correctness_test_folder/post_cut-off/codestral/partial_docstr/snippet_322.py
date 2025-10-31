
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import json


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    environments: Dict[str, Dict[str, Any]] = None
    learning_fields: List[str] = None
    learning_contexts: List[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        # Implementation for creating config from environment variables
        pass

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def validate(self) -> List[str]:
        errors = []
        if not isinstance(self.environments, dict):
            errors.append("environments must be a dictionary")
        if not isinstance(self.learning_fields, list):
            errors.append("learning_fields must be a list")
        if not isinstance(self.learning_contexts, list):
            errors.append("learning_contexts must be a list")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learning_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learning_contexts
