from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def _parse_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    val = value.strip().lower()
    if val in {"1", "true", "yes", "on"}:
        return True
    if val in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_json(value: Optional[str], default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except Exception:
        return default


def _parse_csv(value: Optional[str]) -> Set[str]:
    if not value:
        return set()
    return {part.strip().lower() for part in value.split(",") if part.strip()}


def _to_lower_set(values: Optional[List[str] | Set[str]]) -> Set[str]:
    if not values:
        return set()
    return {str(v).strip().lower() for v in values if str(v).strip()}


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    enabled: bool = True
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    default_environment: Optional[str] = None
    learn_enabled: bool = True
    learn_fields_include: Set[str] = field(default_factory=set)
    learn_fields_exclude: Set[str] = field(default_factory=set)
    learn_contexts_include: Set[str] = field(default_factory=set)
    learn_contexts_exclude: Set[str] = field(default_factory=set)
    version: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        envs = _parse_json(os.getenv("SMART_DEFAULTS_ENVIRONMENTS"), {}) or {}
        # Normalize environment values to dicts
        norm_envs: Dict[str, Dict[str, Any]] = {}
        for k, v in envs.items():
            if isinstance(v, dict):
                norm_envs[str(k)] = v
            else:
                # If provided as non-dict, wrap under "value"
                norm_envs[str(k)] = {"value": v}

        return cls(
            enabled=_parse_bool(os.getenv("SMART_DEFAULTS_ENABLED"), True),
            environments=norm_envs,
            default_environment=os.getenv(
                "SMART_DEFAULTS_DEFAULT_ENVIRONMENT") or None,
            learn_enabled=_parse_bool(
                os.getenv("SMART_DEFAULTS_LEARN_ENABLED"), True),
            learn_fields_include=_parse_csv(
                os.getenv("SMART_DEFAULTS_LEARN_FIELDS_INCLUDE")),
            learn_fields_exclude=_parse_csv(
                os.getenv("SMART_DEFAULTS_LEARN_FIELDS_EXCLUDE")),
            learn_contexts_include=_parse_csv(
                os.getenv("SMART_DEFAULTS_LEARN_CONTEXTS_INCLUDE")),
            learn_contexts_exclude=_parse_csv(
                os.getenv("SMART_DEFAULTS_LEARN_CONTEXTS_EXCLUDE")),
            version=os.getenv("SMART_DEFAULTS_VERSION") or None,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Accept both flat and nested "learn" schema
        enabled = data.get("enabled", True)
        environments = data.get("environments", {}) or {}
        default_environment = data.get("default_environment")
        version = data.get("version")

        learn = data.get("learn", {})
        learn_enabled = learn.get("enabled", data.get("learn_enabled", True))
        fields = learn.get("fields", {})
        contexts = learn.get("contexts", {})

        learn_fields_include = _to_lower_set(fields.get(
            "include", data.get("learn_fields_include")))
        learn_fields_exclude = _to_lower_set(fields.get(
            "exclude", data.get("learn_fields_exclude")))
        learn_contexts_include = _to_lower_set(contexts.get(
            "include", data.get("learn_contexts_include")))
        learn_contexts_exclude = _to_lower_set(contexts.get(
            "exclude", data.get("learn_contexts_exclude")))

        # Normalize environments: ensure dict[str, dict]
        norm_envs: Dict[str, Dict[str, Any]] = {}
        for k, v in environments.items():
            if isinstance(v, dict):
                norm_envs[str(k)] = v
            else:
                norm_envs[str(k)] = {"value": v}

        return cls(
            enabled=bool(enabled),
            environments=norm_envs,
            default_environment=default_environment,
            learn_enabled=bool(learn_enabled),
            learn_fields_include=learn_fields_include,
            learn_fields_exclude=learn_fields_exclude,
            learn_contexts_include=learn_contexts_include,
            learn_contexts_exclude=learn_contexts_exclude,
            version=version,
        )

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        config_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "enabled": self.enabled,
            "version": self.version,
            "default_environment": self.default_environment,
            "environments": self.environments,
            "learn": {
                "enabled": self.learn_enabled,
                "fields": {
                    "include": sorted(self.learn_fields_include),
                    "exclude": sorted(self.learn_fields_exclude),
                },
                "contexts": {
                    "include": sorted(self.learn_contexts_include),
                    "exclude": sorted(self.learn_contexts_exclude),
                },
            },
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues: List[str] = []

        if not isinstance(self.enabled, bool):
            issues.append("enabled must be a boolean")

        if not isinstance(self.learn_enabled, bool):
            issues.append("learn_enabled must be a boolean")

        if not isinstance(self.environments, dict):
            issues.append("environments must be a dict[str, dict]")
        else:
            for k, v in self.environments.items():
                if not isinstance(k, str):
                    issues.append("environment keys must be strings")
                    break
                if not isinstance(v, dict):
                    issues.append(f"environment '{k}' must map to a dict")
        if self.default_environment and self.default_environment not in self.environments:
            issues.append(
                f"default_environment '{self.default_environment}' not found in environments")

        # Check includes/excludes intersections
        inter_fields = self.learn_fields_include & self.learn_fields_exclude
        if inter_fields:
            issues.append(
                f"fields present in both include and exclude: {sorted(inter_fields)}")
        inter_contexts = self.learn_contexts_include & self.learn_contexts_exclude
        if inter_contexts:
            issues.append(
                f"contexts present in both include and exclude: {sorted(inter_contexts)}")

        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        env = environment or ""
        base = self.environments.get("default", {}) or {}
        specific = self.environments.get(env, {}) or {}
        # Shallow overlay of specific on top of base
        result = dict(base)
        result.update(specific)
        return result

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        if not (self.enabled and self.learn_enabled):
            return False
        name = (field_name or "").strip().lower()
        if not name:
            return False
        if self.learn_fields_include:
            return name in self.learn_fields_include and name not in self.learn_fields_exclude
        return name not in self.learn_fields_exclude

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        if not (self.enabled and self.learn_enabled):
            return False
        ctx = (context or "").strip().lower()
        if not ctx:
            return False
        if self.learn_contexts_include:
            return ctx in self.learn_contexts_include and ctx not in self.learn_contexts_exclude
        return ctx not in self.learn_contexts_exclude
