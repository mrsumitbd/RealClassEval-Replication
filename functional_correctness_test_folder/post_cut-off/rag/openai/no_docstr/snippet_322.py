
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SmartDefaultsConfig:
    """Configuration for Smart Defaults system"""

    defaults: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_fields: List[str] = field(default_factory=list)
    learn_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        """Create configuration from environment variables"""
        # Environment variable names
        env_defaults = os.getenv("SMART_DEFAULTS_DEFAULTS")
        env_learn_fields = os.getenv("SMART_DEFAULTS_LEARN_FIELDS")
        env_learn_contexts = os.getenv("SMART_DEFAULTS_LEARN_CONTEXTS")

        defaults: Dict[str, Dict[str, Any]] = {}
        if env_defaults:
            try:
                defaults = json.loads(env_defaults)
                if not isinstance(defaults, dict):
                    defaults = {}
            except Exception:
                defaults = {}

        learn_fields: List[str] = []
        if env_learn_fields:
            try:
                learn_fields = json.loads(env_learn_fields)
                if not isinstance(learn_fields, list):
                    learn_fields = []
            except Exception:
                learn_fields = []

        learn_contexts: List[str] = []
        if env_learn_contexts:
            try:
                learn_contexts = json.loads(env_learn_contexts)
                if not isinstance(learn_contexts, list):
                    learn_contexts = []
            except Exception:
                learn_contexts = []

        return cls(
            defaults=defaults,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """Load configuration from JSON file"""
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        defaults = data.get("defaults", {})
        learn_fields = data.get("learn_fields", [])
        learn_contexts = data.get("learn_contexts", [])

        return cls(
            defaults=defaults,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts,
        )

    def to_file(self, config_path: Path):
        """Save configuration to JSON file"""
        data: Dict[str, Any] = {
            "defaults": self.defaults,
            "learn_fields": self.learn_fields,
            "learn_contexts": self.learn_contexts,
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues: List[str] = []

        if not isinstance(self.defaults, dict):
            issues.append("`defaults` must be a dictionary")
        else:
            for env, env_defaults in self.defaults.items():
                if not isinstance(env_defaults, dict):
                    issues.append(
                        f"Defaults for environment '{env}' must be a dictionary")

        if not isinstance(self.learn_fields, list):
            issues.append("`learn_fields` must be a list")
        else:
            for field_name in self.learn_fields:
                if not isinstance(field_name, str):
                    issues.append(
                        f"Learn field '{field_name}' must be a string")

        if not isinstance(self.learn_contexts, list):
            issues.append("`learn_contexts` must be a list")
        else:
            for context in self.learn_contexts:
                if not isinstance(context, str):
                    issues.append(
                        f"Learn context '{context}' must be a string")

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """Get defaults for a specific environment"""
        return self.defaults.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """Check if learning should be enabled for a field"""
        return field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        """Check if learning should be enabled for a context"""
        return context in self.learn_contexts
