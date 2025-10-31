
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SmartDefaultsConfig:
    """
    Configuration for Smart Defaults system.
    """
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

        Environment variables expected:
            SMART_DEFAULTS_CONFIG_JSON   - JSON string of the whole config
            SMART_DEFAULTS_ENVIRONMENTS  - JSON string of environments mapping
            SMART_DEFAULTS_LEARN_FIELDS  - comma‑separated list of field names
            SMART_DEFAULTS_LEARN_CONTEXTS - comma‑separated list of context names
        """
        # Prefer a single JSON config if provided
        json_str = os.getenv("SMART_DEFAULTS_CONFIG_JSON")
        if json_str:
            try:
                data = json.loads(json_str)
                return cls.from_dict(data)
            except json.JSONDecodeError:
                pass  # fall back to individual vars

        # Build config from individual env vars
        envs_json = os.getenv("SMART_DEFAULTS_ENVIRONMENTS", "{}")
        try:
            environments = json.loads(envs_json)
        except json.JSONDecodeError:
            environments = {}

        learn_fields = os.getenv("SMART_DEFAULTS_LEARN_FIELDS", "")
        learn_fields = [f.strip()
                        for f in learn_fields.split(",") if f.strip()]

        learn_contexts = os.getenv("SMART_DEFAULTS_LEARN_CONTEXTS", "")
        learn_contexts = [c.strip()
                          for c in learn_contexts.split(",") if c.strip()]

        return cls(
            environments=environments,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """
        Load configuration from JSON file.
        """
        if not config_path.is_file():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SmartDefaultsConfig":
        """
        Helper to create an instance from a dictionary.
        """
        environments = data.get("environments", {})
        learn_fields = data.get("learn_fields", [])
        learn_contexts = data.get("learn_contexts", [])
        return cls(
            environments=environments,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts,
        )

    def to_file(self, config_path: Path):
        """
        Save configuration to JSON file.
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "environments": self.environments,
                    "learn_fields": self.learn_fields,
                    "learn_contexts": self.learn_contexts,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

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

        if not isinstance(self.learn_fields, list):
            issues.append("`learn_fields` must be a list.")
        else:
            for field_name in self.learn_fields:
                if not isinstance(field_name, str):
                    issues.append(
                        f"Learn field `{field_name}` is not a string.")

        if not isinstance(self.learn_contexts, list):
            issues.append("`learn_contexts` must be a list.")
        else:
            for ctx in self.learn_contexts:
                if not isinstance(ctx, str):
                    issues.append(f"Learn context `{ctx}` is not a string.")

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
        return field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        """
        Check if learning should be enabled for a context.
        """
        return context in self.learn_contexts
