
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
import json
import os


@dataclass
class SmartDefaultsConfig:
    environments: Dict[str, Dict[str, Any]]
    learn_from_fields: List[str]
    learn_from_contexts: List[str]

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        config_path = Path(os.environ.get(
            'SMART_DEFAULTS_CONFIG_PATH', 'smart_defaults_config.json'))
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
        for environment, defaults in self.environments.items():
            if not isinstance(defaults, dict):
                errors.append(
                    f"Defaults for environment '{environment}' must be a dictionary")
        if not isinstance(self.learn_from_fields, list):
            errors.append("learn_from_fields must be a list")
        if not isinstance(self.learn_from_contexts, list):
            errors.append("learn_from_contexts must be a list")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learn_from_contexts
