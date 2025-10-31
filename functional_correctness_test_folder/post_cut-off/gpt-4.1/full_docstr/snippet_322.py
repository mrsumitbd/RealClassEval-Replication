
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from pathlib import Path
import os
import json


@dataclass
class SmartDefaultsConfig:
    '''Configuration for Smart Defaults system'''
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_fields: List[str] = field(default_factory=list)
    learn_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> 'SmartDefaultsConfig':
        '''Create configuration from environment variables'''
        envs = os.environ.get("SMART_DEFAULTS_ENVIRONMENTS", "")
        fields = os.environ.get("SMART_DEFAULTS_LEARN_FIELDS", "")
        contexts = os.environ.get("SMART_DEFAULTS_LEARN_CONTEXTS", "")

        environments = {}
        if envs:
            # Expecting: ENV1:key1=val1,key2=val2;ENV2:key3=val3
            for envdef in envs.split(";"):
                if not envdef.strip():
                    continue
                if ":" not in envdef:
                    continue
                env_name, kvs = envdef.split(":", 1)
                env_dict = {}
                for kv in kvs.split(","):
                    if "=" in kv:
                        k, v = kv.split("=", 1)
                        env_dict[k.strip()] = v.strip()
                environments[env_name.strip()] = env_dict

        learn_fields = [f.strip() for f in fields.split(",")
                        if f.strip()] if fields else []
        learn_contexts = [c.strip() for c in contexts.split(
            ",") if c.strip()] if contexts else []

        return cls(
            environments=environments,
            learn_fields=learn_fields,
            learn_contexts=learn_contexts
        )

    @classmethod
    def from_file(cls, config_path: Path) -> 'SmartDefaultsConfig':
        '''Load configuration from JSON file'''
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            environments=data.get("environments", {}),
            learn_fields=data.get("learn_fields", []),
            learn_contexts=data.get("learn_contexts", [])
        )

    def to_file(self, config_path: Path):
        '''Save configuration to JSON file'''
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)

    def validate(self) -> List[str]:
        '''Validate configuration and return list of issues'''
        issues = []
        if not isinstance(self.environments, dict):
            issues.append("environments must be a dictionary")
        else:
            for env, vals in self.environments.items():
                if not isinstance(env, str):
                    issues.append(f"Environment name '{env}' is not a string")
                if not isinstance(vals, dict):
                    issues.append(
                        f"Environment '{env}' values must be a dictionary")
        if not isinstance(self.learn_fields, list):
            issues.append("learn_fields must be a list")
        else:
            for f in self.learn_fields:
                if not isinstance(f, str):
                    issues.append(f"learn_fields entry '{f}' is not a string")
        if not isinstance(self.learn_contexts, list):
            issues.append("learn_contexts must be a list")
        else:
            for c in self.learn_contexts:
                if not isinstance(c, str):
                    issues.append(
                        f"learn_contexts entry '{c}' is not a string")
        return issues

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        '''Get defaults for a specific environment'''
        return self.environments.get(environment, {}).copy()

    def should_learn_from_field(self, field_name: str) -> bool:
        '''Check if learning should be enabled for a field'''
        return field_name in self.learn_fields

    def should_learn_from_context(self, context: str) -> bool:
        '''Check if learning should be enabled for a context'''
        return context in self.learn_contexts
