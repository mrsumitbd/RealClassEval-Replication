
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""

    # Mapping of environment name to its default values
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # List of field names that should be learned from
    learn_fields: List[str] = field(default_factory=list)

    # List of context names that should be learned from
    learn_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        """
        Create configuration from environment variables.

        Environment variables supported:
            - SMART_DEFAULTS_CONFIG_JSON: JSON string of the config.
            - SMART_DEFAULTS_CONFIG_PATH: Path to a JSON file containing the config.
        """
        json_str = os.getenv("SMART_DEFAULTS_CONFIG_JSON")
        if json_str:
            try:
                data = json.loads(json_str)
                return cls.from_dict(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in SMART_DEFAULTS_CONFIG_JSON")

        path_str = os.getenv("SMART_DEFAULTS_CONFIG_PATH")
        if path_str:
            return cls.from_file(Path(path_str))

        # No config provided – return an empty config
        return cls()

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """Load configuration from JSON file."""
        if not config_path.is_file():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_file(self, config_path: Path) -> None:
        """Save configuration to JSON file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, sort_keys=True)

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues: List[str] = []

        if not isinstance(self.environments, dict):
            issues.append("`environments` must be a dict")

        if not isinstance(self.learn_fields, list):
            issues.append("`learn_fields` must be a list")
        else:
            for field_name in self.learn_fields:
                if not isinstance(field_name, str):
                    issues.append(
                        f"learn_fields contains non-string value: {field_name!r}")

        if not isinstance(self.learn_contexts, list):
            issues.append("`learn_contexts` must be a list")
        else:
            for ctx in self.learn_contexts:
                if not isinstance(ctx, str):
                    issues.append(
                        f"learn_contexts contains non-string value: {ctx!r}")

        # Validate each environment's defaults
        for env, defaults in self.environments.items():
            if not isinstance(env, str):
                issues.append(f"Environment key is not a string: {env!r}")
            if not isinstance(defaults, dict):
                issues.append(
                    f"Defaults for environment '{env}' must be a dict")

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment."""
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field."""
        return field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context."""
        return context in self.learn_contexts

    # Helper methods for (de)serialization
    def to_dict(self) -> Dict[str, Any]:
        return {
            "environments": self.environments,
            "learn_fields": self.learn_fields,
            "learn_contexts": self.learn_contexts,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SmartDefaultsConfig":
        return cls(
            environments=data.get("environments", {}),
            learn_fields=data.get("learn_fields", []),
            learn_contexts=data.get("learn_contexts", []),
        )
