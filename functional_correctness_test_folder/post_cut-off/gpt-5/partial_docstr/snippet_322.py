from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    version: str = "1"
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    learn_enabled: bool = True
    learn_fields_include: Set[str] = field(default_factory=set)
    learn_fields_exclude: Set[str] = field(default_factory=set)
    learn_contexts_include: Set[str] = field(default_factory=set)
    learn_contexts_exclude: Set[str] = field(default_factory=set)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        file_var = os.environ.get(
            "SMART_DEFAULTS_FILE") or os.environ.get("SD_CONFIG_FILE")
        if file_var:
            return cls.from_file(Path(file_var))

        def _truthy(val: Optional[str], default: bool = True) -> bool:
            if val is None:
                return default
            return val.strip().lower() not in {"0", "false", "no", "off"}

        def _as_set(var_name: str) -> Set[str]:
            raw = os.environ.get(var_name, "")
            if not raw:
                return set()
            return {item.strip() for item in raw.split(",") if item.strip()}

        cfg = cls()
        cfg.version = os.environ.get("SD_VERSION", cfg.version)

        envs_raw = os.environ.get("SD_ENVIRONMENTS")
        if envs_raw:
            try:
                parsed = json.loads(envs_raw)
                if isinstance(parsed, dict):
                    # Ensure inner values are dicts
                    cfg.environments = {
                        str(k): (v if isinstance(v, dict) else {}) for k, v in parsed.items()
                    }
            except json.JSONDecodeError:
                pass  # ignore invalid env var

        cfg.learn_enabled = _truthy(os.environ.get(
            "SD_LEARN_ENABLED"), default=cfg.learn_enabled)
        cfg.learn_fields_include = _as_set("SD_FIELDS_INCLUDE")
        cfg.learn_fields_exclude = _as_set("SD_FIELDS_EXCLUDE")
        cfg.learn_contexts_include = _as_set("SD_CONTEXTS_INCLUDE")
        cfg.learn_contexts_exclude = _as_set("SD_CONTEXTS_EXCLUDE")

        return cfg

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        suffix = config_path.suffix.lower()
        text = config_path.read_text(encoding="utf-8")

        data: Dict[str, Any]
        if suffix == ".json":
            data = json.loads(text)
        elif suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise RuntimeError(
                    "PyYAML is required to load YAML configuration files.")
            loaded = yaml.safe_load(text)
            data = loaded if isinstance(loaded, dict) else {}
        else:
            # Try JSON first, then YAML if available
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                if yaml is None:
                    raise ValueError(
                        "Unknown config format and YAML not available.")
                loaded = yaml.safe_load(text)
                data = loaded if isinstance(loaded, dict) else {}

        cfg = cls()
        # Accept both flat and nested "learn" structure
        cfg.version = str(data.get("version", cfg.version))
        cfg.environments = {
            str(k): (v if isinstance(v, dict) else {})
            for k, v in (data.get("environments") or {}).items()
        }

        # Flat keys
        if "learn_enabled" in data:
            cfg.learn_enabled = bool(data["learn_enabled"])
        if "learn_fields_include" in data:
            cfg.learn_fields_include = set(
                map(str, data.get("learn_fields_include") or []))
        if "learn_fields_exclude" in data:
            cfg.learn_fields_exclude = set(
                map(str, data.get("learn_fields_exclude") or []))
        if "learn_contexts_include" in data:
            cfg.learn_contexts_include = set(
                map(str, data.get("learn_contexts_include") or []))
        if "learn_contexts_exclude" in data:
            cfg.learn_contexts_exclude = set(
                map(str, data.get("learn_contexts_exclude") or []))

        # Nested "learn" block
        learn = data.get("learn")
        if isinstance(learn, dict):
            if "enabled" in learn:
                cfg.learn_enabled = bool(learn.get("enabled"))
            fields = learn.get("fields")
            if isinstance(fields, dict):
                if "include" in fields:
                    cfg.learn_fields_include = set(
                        map(str, fields.get("include") or []))
                if "exclude" in fields:
                    cfg.learn_fields_exclude = set(
                        map(str, fields.get("exclude") or []))
            contexts = learn.get("contexts")
            if isinstance(contexts, dict):
                if "include" in contexts:
                    cfg.learn_contexts_include = set(
                        map(str, contexts.get("include") or []))
                if "exclude" in contexts:
                    cfg.learn_contexts_exclude = set(
                        map(str, contexts.get("exclude") or []))

        return cfg

    def to_file(self, config_path: Path):
        config_path.parent.mkdir(parents=True, exist_ok=True)
        payload: Dict[str, Any] = {
            "version": self.version,
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

        suffix = config_path.suffix.lower()
        if suffix == ".json":
            config_path.write_text(json.dumps(
                payload, indent=2, sort_keys=True), encoding="utf-8")
        elif suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise RuntimeError(
                    "PyYAML is required to write YAML configuration files.")
            config_path.write_text(yaml.safe_dump(
                payload, sort_keys=False), encoding="utf-8")
        else:
            # Default to JSON
            config_path.write_text(json.dumps(
                payload, indent=2, sort_keys=True), encoding="utf-8")

    def validate(self) -> List[str]:
        errors: List[str] = []

        if not isinstance(self.version, str) or not self.version.strip():
            errors.append("version must be a non-empty string")

        if not isinstance(self.environments, dict):
            errors.append("environments must be a dict")
        else:
            for name, defaults in self.environments.items():
                if not isinstance(name, str) or not name.strip():
                    errors.append(
                        "environment names must be non-empty strings")
                if not isinstance(defaults, dict):
                    errors.append(
                        f"environment '{name}' defaults must be a dict")

        if not isinstance(self.learn_enabled, bool):
            errors.append("learn_enabled must be a boolean")

        # Validate sets are actually sets of strings
        def _ensure_set_str(value: Any, label: str):
            if not isinstance(value, (set, frozenset)):
                errors.append(f"{label} must be a set")
                return
            for v in value:
                if not isinstance(v, str):
                    errors.append(f"all values in {label} must be strings")
                    break

        _ensure_set_str(self.learn_fields_include, "learn_fields_include")
        _ensure_set_str(self.learn_fields_exclude, "learn_fields_exclude")
        _ensure_set_str(self.learn_contexts_include, "learn_contexts_include")
        _ensure_set_str(self.learn_contexts_exclude, "learn_contexts_exclude")

        # Overlap checks
        overlap_fields = self.learn_fields_include & self.learn_fields_exclude
        if overlap_fields:
            errors.append(
                f"fields cannot be both included and excluded: {sorted(overlap_fields)}"
            )
        overlap_contexts = self.learn_contexts_include & self.learn_contexts_exclude
        if overlap_contexts:
            errors.append(
                f"contexts cannot be both included and excluded: {sorted(overlap_contexts)}"
            )

        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        defaults = self.environments.get(environment, {})
        return dict(defaults)

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        if not self.learn_enabled:
            return False
        if self.learn_fields_include:
            return field_name in self.learn_fields_include
        return field_name not in self.learn_fields_exclude

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        if not self.learn_enabled:
            return False
        if self.learn_contexts_include:
            return context in self.learn_contexts_include
        return context not in self.learn_contexts_exclude
