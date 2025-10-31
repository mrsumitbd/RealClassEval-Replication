
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""

    # Mapping of environment name to its default key/value pairs
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Set of field names that should be learned from
    learn_fields: Set[str] = field(default_factory=set)

    # Set of context names that should be learned from
    learn_contexts: Set[str] = field(default_factory=set)

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        """
        Create configuration from environment variables.

        The environment variable `SMART_DEFAULTS_CONFIG` may contain a JSON
        string representing the configuration. If the variable is not set,
        an empty configuration is returned.
        """
        json_str = os.getenv("SMART_DEFAULTS_CONFIG")
        if not json_str:
            return cls()
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in SMART_DEFAULTS_CONFIG: {exc}") from exc
        return cls._from_dict(data)

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """
        Load configuration from JSON file.
        """
        if not config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {config_path}: {exc}") from exc
        return cls._from_dict(data)

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "SmartDefaultsConfig":
        """
        Helper to create an instance from a dictionary.
        """
        envs = data.get("environments", {})
        if not isinstance(envs, dict):
            envs = {}
        learn_fields = data.get("learn_fields", [])
        if not isinstance(learn_fields, list):
            learn_fields = []
        learn_contexts = data.get("learn_contexts", [])
        if not isinstance(learn_contexts, list):
            learn_contexts = []
        return cls(
            environments=envs,
            learn_fields=set(learn_fields),
            learn_contexts=set(learn_contexts),
        )

    def to_file(self, config_path: Path):
        """
        Save configuration to JSON file.
        """
        data = {
            "environments": self.environments,
            "learn_fields": sorted(self.learn_fields),
            "learn_contexts": sorted(self.learn_contexts),
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def validate(self) -> List[str]:
        """
        Validate configuration and return list of issues.
        """
        issues: List[str] = []

        if not isinstance(self.environments, dict):
            issues.append("`environments` must be a dictionary.")
        else:
            for env, defaults in self.environments.items():
                if not isinstance(env, str):
                    issues.append(f"Environment key `{env}` is not a string.")
                if not isinstance(defaults, dict):
                    issues.append(
                        f"Defaults for environment `{env}` must be a dictionary.")

        if not isinstance(self.learn_fields, set):
            issues.append("`learn_fields` must be a set.")
        else:
            for field_name in self.learn_fields:
                if not isinstance(field_name, str):
                    issues.append(
                        f"Learn field `{field_name}` is not a string.")

        if not isinstance(self.learn_contexts, set):
            issues.append("`learn_contexts` must be a set.")
        else:
            for context in self.learn_contexts:
                if not isinstance(context, str):
                    issues.append(
                        f"Learn context `{context}` is not a string.")

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """
        Get defaults for a specific environment.
        """
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """
        Check if learning should be enabled for a field.
        """
        if "*" in self.learn_fields:
            return True
        return field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        """
        Check if learning should be enabled for a context.
        """
        if "*" in self.learn_contexts:
            return True
        return context in self.learn_contexts
