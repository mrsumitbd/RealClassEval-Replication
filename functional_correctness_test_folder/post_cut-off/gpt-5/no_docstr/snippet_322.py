from __future__ import annotations

import json
import os
import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


def _parse_bool(val: Optional[str], default: bool = True) -> bool:
    if val is None:
        return default
    v = val.strip().lower()
    if v in {"1", "true", "yes", "on"}:
        return True
    if v in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_csv(val: Optional[str]) -> Optional[List[str]]:
    if val is None:
        return None
    items = [x.strip() for x in val.split(",")]
    return [x for x in items if x]


@dataclass
class SmartDefaultsConfig:
    enabled: bool = True
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_field_allowlist: Optional[List[str]] = None
    learn_field_denylist: Optional[List[str]] = None
    learn_context_allowlist: Optional[List[str]] = None
    learn_context_denylist: Optional[List[str]] = None

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        enabled = _parse_bool(os.environ.get("SMART_DEFAULTS_ENABLED"), True)

        field_allow = _parse_csv(os.environ.get(
            "SMART_DEFAULTS_FIELD_ALLOWLIST"))
        field_deny = _parse_csv(os.environ.get(
            "SMART_DEFAULTS_FIELD_DENYLIST"))

        ctx_allow = _parse_csv(os.environ.get(
            "SMART_DEFAULTS_CONTEXT_ALLOWLIST"))
        ctx_deny = _parse_csv(os.environ.get(
            "SMART_DEFAULTS_CONTEXT_DENYLIST"))

        env_defaults: Dict[str, Dict[str, Any]] = {}
        # Prefer a single JSON blob definition
        raw_envs = os.environ.get("SMART_DEFAULTS_ENVIRONMENTS")
        if raw_envs:
            try:
                parsed = json.loads(raw_envs)
                if isinstance(parsed, dict):
                    for k, v in parsed.items():
                        if isinstance(v, dict):
                            env_defaults[str(k)] = v
            except json.JSONDecodeError:
                pass

        # Also allow per-environment variables like SMART_DEFAULTS_ENV_PROD='{"key":"val"}'
        prefix = "SMART_DEFAULTS_ENV_"
        for key, val in os.environ.items():
            if key.startswith(prefix):
                env_name = key[len(prefix):].strip()
                if not env_name:
                    continue
                try:
                    parsed_env = json.loads(val)
                    if isinstance(parsed_env, dict):
                        env_defaults[env_name] = parsed_env
                except json.JSONDecodeError:
                    continue

        return cls(
            enabled=enabled,
            environments=env_defaults,
            learn_field_allowlist=field_allow,
            learn_field_denylist=field_deny,
            learn_context_allowlist=ctx_allow,
            learn_context_denylist=ctx_deny,
        )

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        data: Dict[str, Any]
        text = config_path.read_text(encoding="utf-8")
        data = json.loads(text)

        enabled = bool(data.get("enabled", True))
        environments = data.get("environments", {}) or {}
        field_allow = data.get("learn_field_allowlist")
        field_deny = data.get("learn_field_denylist")
        ctx_allow = data.get("learn_context_allowlist")
        ctx_deny = data.get("learn_context_denylist")

        return cls(
            enabled=enabled,
            environments=environments if isinstance(
                environments, dict) else {},
            learn_field_allowlist=list(field_allow) if isinstance(
                field_allow, list) else None,
            learn_field_denylist=list(field_deny) if isinstance(
                field_deny, list) else None,
            learn_context_allowlist=list(ctx_allow) if isinstance(
                ctx_allow, list) else None,
            learn_context_denylist=list(ctx_deny) if isinstance(
                ctx_deny, list) else None,
        )

    def to_file(self, config_path: Path):
        payload = {
            "enabled": self.enabled,
            "environments": self.environments,
            "learn_field_allowlist": self.learn_field_allowlist,
            "learn_field_denylist": self.learn_field_denylist,
            "learn_context_allowlist": self.learn_context_allowlist,
            "learn_context_denylist": self.learn_context_denylist,
        }
        config_path.write_text(json.dumps(
            payload, indent=2, sort_keys=True), encoding="utf-8")

    def validate(self) -> List[str]:
        errors: List[str] = []

        if not isinstance(self.enabled, bool):
            errors.append("enabled must be a boolean")

        if not isinstance(self.environments, dict):
            errors.append(
                "environments must be a dict of environment -> defaults dict")
        else:
            for env, defaults in self.environments.items():
                if not isinstance(env, str):
                    errors.append("environment names must be strings")
                if not isinstance(defaults, dict):
                    errors.append(
                        f"defaults for environment '{env}' must be a dict")

        def _validate_list(name: str, value: Optional[List[str]]):
            if value is not None and not isinstance(value, list):
                errors.append(f"{name} must be a list of strings")
            elif value is not None:
                for i, v in enumerate(value):
                    if not isinstance(v, str):
                        errors.append(f"{name}[{i}] must be a string")

        _validate_list("learn_field_allowlist", self.learn_field_allowlist)
        _validate_list("learn_field_denylist", self.learn_field_denylist)
        _validate_list("learn_context_allowlist", self.learn_context_allowlist)
        _validate_list("learn_context_denylist", self.learn_context_denylist)

        # Overlap checks (only when exact same string appears in both)
        if self.learn_field_allowlist and self.learn_field_denylist:
            overlap = set(self.learn_field_allowlist) & set(
                self.learn_field_denylist)
            if overlap:
                errors.append(
                    f"field allowlist and denylist overlap: {sorted(overlap)}")

        if self.learn_context_allowlist and self.learn_context_denylist:
            overlap = set(self.learn_context_allowlist) & set(
                self.learn_context_denylist)
            if overlap:
                errors.append(
                    f"context allowlist and denylist overlap: {sorted(overlap)}")

        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        return dict(self.environments.get(environment, {}))

    def should_learn_from_field(self, field_name: str) -> bool:
        if not self.enabled:
            return False
        if self.learn_field_denylist:
            for pat in self.learn_field_denylist:
                if fnmatch.fnmatch(field_name, pat):
                    return False
        if self.learn_field_allowlist:
            for pat in self.learn_field_allowlist:
                if fnmatch.fnmatch(field_name, pat):
                    return True
            return False
        return True

    def should_learn_from_context(self, context: str) -> bool:
        if not self.enabled:
            return False
        if self.learn_context_denylist:
            for pat in self.learn_context_denylist:
                if fnmatch.fnmatch(context, pat):
                    return False
        if self.learn_context_allowlist:
            for pat in self.learn_context_allowlist:
                if fnmatch.fnmatch(context, pat):
                    return True
            return False
        return True
