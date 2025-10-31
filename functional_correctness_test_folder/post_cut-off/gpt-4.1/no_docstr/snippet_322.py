
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import os
import json


@dataclass
class SmartDefaultsConfig:
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_from_fields: List[str] = field(default_factory=list)
    learn_from_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        envs = os.environ.get("SMART_DEFAULTS_ENVIRONMENTS")
        fields = os.environ.get("SMART_DEFAULTS_LEARN_FIELDS")
        contexts = os.environ.get("SMART_DEFAULTS_LEARN_CONTEXTS")
        environments = {}
        if envs:
            try:
                environments = json.loads(envs)
            except Exception:
                environments = {}
        learn_from_fields = fields.split(",") if fields else []
        learn_from_contexts = contexts.split(",") if contexts else []
        return cls(
            environments=environments,
            learn_from_fields=[f.strip()
                               for f in learn_from_fields if f.strip()],
            learn_from_contexts=[c.strip()
                                 for c in learn_from_contexts if c.strip()]
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        environments = data.get("environments", {})
        learn_from_fields = data.get("learn_from_fields", [])
        learn_from_contexts = data.get("learn_from_contexts", [])
        return cls(
            environments=environments,
            learn_from_fields=learn_from_fields,
            learn_from_contexts=learn_from_contexts
        )

    def to_file(self, config_path: Path):
        data = {
            "environments": self.environments,
            "learn_from_fields": self.learn_from_fields,
            "learn_from_contexts": self.learn_from_contexts
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self) -> List[str]:
        errors = []
        if not isinstance(self.environments, dict):
            errors.append("environments must be a dictionary")
        if not isinstance(self.learn_from_fields, list):
            errors.append("learn_from_fields must be a list")
        if not isinstance(self.learn_from_contexts, list):
            errors.append("learn_from_contexts must be a list")
        for env, defaults in self.environments.items():
            if not isinstance(defaults, dict):
                errors.append(
                    f"Defaults for environment '{env}' must be a dictionary")
        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        return context in self.learn_from_contexts
