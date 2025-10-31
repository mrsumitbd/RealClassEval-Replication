
from dataclasses import dataclass, field
from typing import List, Dict, Any
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
        envs = os.getenv('SMART_DEFAULTS_ENVIRONMENTS', '{}')
        fields = os.getenv('SMART_DEFAULTS_LEARNABLE_FIELDS', '[]')
        contexts = os.getenv('SMART_DEFAULTS_LEARNABLE_CONTEXTS', '[]')
        return cls(
            environments=json.loads(envs),
            learnable_fields=json.loads(fields),
            learnable_contexts=json.loads(contexts)
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with config_path.open('r') as file:
            config_data = json.load(file)
        return cls(**config_data)

    def to_file(self, config_path: Path):
        with config_path.open('w') as file:
            json.dump(self.__dict__, file, indent=4)

    def validate(self) -> List[str]:
        errors = []
        if not isinstance(self.environments, dict):
            errors.append("environments must be a dictionary")
        if not isinstance(self.learnable_fields, list):
            errors.append("learnable_fields must be a list")
        if not isinstance(self.learnable_contexts, list):
            errors.append("learnable_contexts must be a list")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learnable_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learnable_contexts
