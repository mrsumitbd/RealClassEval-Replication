
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""

    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_fields: Set[str] = field(default_factory=set)
    learn_contexts: Set[str] = field(default_factory=set)

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        """Create a config from the SMART_DEFAULTS_CONFIG environment variable."""
        env_var = os.getenv("SMART_DEFAULTS_CONFIG")
        if not env_var:
            return cls()
        try:
            data = json.loads(env_var)
        except json.JSONDecodeError:
            # If the env var is not valid JSON, fall back to empty config
            return cls()
        return cls._from_dict(data)

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """Create a config from a JSON file."""
        if not config_path.is_file():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls._from_dict(data)

    def to_file(self, config_path: Path):
        """Write the config to a JSON file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "environments": self.environments,
                    "learn_fields": sorted(self.learn_fields),
                    "learn_contexts": sorted(self.learn_contexts),
                },
                f,
                indent=2,
                sort_keys=True,
            )

    def validate(self) -> List[str]:
        """Validate the configuration and return a list of error messages."""
        errors: List[str] = []

        if not isinstance(self.environments, dict):
            errors.append("environments must be a dict")
        else:
            for env, defaults in self.environments.items():
                if not isinstance(env, str):
                    errors.append(f"environment key {env!r} is not a string")
                if not isinstance(defaults, dict):
                    errors.append(
                        f"defaults for environment {env!r} must be a dict")

        if not isinstance(self.learn_fields, set):
            errors.append("learn_fields must be a set")
        else:
            for field_name in self.learn_fields:
                if not isinstance(field_name, str):
                    errors.append(
                        f"learn_fields contains non-string value {field_name!r}")

        if not isinstance(self.learn_contexts, set):
            errors.append("learn_contexts must be a set")
        else:
            for context in self.learn_contexts:
                if not isinstance(context, str):
                    errors.append(
                        f"learn_contexts contains non-string value {context!r}")

        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment."""
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field."""
        return "*" in self.learn_fields or field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context."""
        return "*" in self.learn_contexts or context in self.learn_contexts

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "SmartDefaultsConfig":
        """Internal helper to create a config from a dictionary."""
        envs = data.get("environments", {})
        learn_fields = set(data.get("learn_fields", []))
        learn_contexts = set(data.get("learn_contexts", []))
        return cls(
            environments=envs,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts,
        )
