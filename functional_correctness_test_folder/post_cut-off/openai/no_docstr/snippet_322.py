
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class SmartDefaultsConfig:
    """
    Configuration for SmartDefaults.

    Attributes
    ----------
    environments : Dict[str, Dict[str, Any]]
        Mapping of environment names to their default key/value pairs.
    learn_from_fields : List[str]
        List of field names that should be considered for learning.
    learn_from_contexts : List[str]
        List of context identifiers that should be considered for learning.
    """

    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    learn_from_fields: List[str] = field(default_factory=list)
    learn_from_contexts: List[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "SmartDefaultsConfig":
        """
        Create a configuration instance from environment variables.

        The environment variable `SMART_DEFAULTS_CONFIG_PATH` can be used to
        specify a JSON file containing the configuration. If the variable is
        not set, an empty configuration is returned.
        """
        config_path = os.getenv("SMART_DEFAULTS_CONFIG_PATH")
        if config_path:
            return cls.from_file(Path(config_path))
        return cls()

    @classmethod
    def from_file(cls, config_path: Path) -> "SmartDefaultsConfig":
        """
        Load configuration from a JSON file.

        Parameters
        ----------
        config_path : Path
            Path to the JSON configuration file.

        Returns
        -------
        SmartDefaultsConfig
            The loaded configuration instance.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        json.JSONDecodeError
            If the file contents are not valid JSON.
        """
        if not config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract known keys, ignore unknown ones
        envs = data.get("environments", {})
        fields = data.get("learn_from_fields", [])
        contexts = data.get("learn_from_contexts", [])

        # Ensure types are correct
        if not isinstance(envs, dict):
            envs = {}
        if not isinstance(fields, list):
            fields = []
        if not isinstance(contexts, list):
            contexts = []

        return cls(
            environments=envs,
            learn_from_fields=fields,
            learn_from_contexts=contexts,
        )

    def to_file(self, config_path: Path):
        """
        Write the current configuration to a JSON file.

        Parameters
        ----------
        config_path : Path
            Destination file path. The parent directory is created if it does not
            exist.
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "environments": self.environments,
            "learn_from_fields": self.learn_from_fields,
            "learn_from_contexts": self.learn_from_contexts,
        }
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def validate(self) -> List[str]:
        """
        Validate the configuration.

        Returns
        -------
        List[str]
            A list of error messages. An empty list indicates a valid
            configuration.
        """
        errors: List[str] = []

        if not isinstance(self.environments, dict):
            errors.append("`environments` must be a dictionary.")
        else:
            for env, defaults in self.environments.items():
                if not isinstance(env, str):
                    errors.append(f"Environment key `{env}` is not a string.")
                if not isinstance(defaults, dict):
                    errors.append(
                        f"Defaults for environment `{env}` must be a dictionary.")

        if not isinstance(self.learn_from_fields, list):
            errors.append("`learn_from_fields` must be a list.")
        else:
            for field_name in self.learn_from_fields:
                if not isinstance(field_name, str):
                    errors.append(
                        f"Field name `{field_name}` in `learn_from_fields` is not a string.")

        if not isinstance(self.learn_from_contexts, list):
            errors.append("`learn_from_contexts` must be a list.")
        else:
            for context in self.learn_from_contexts:
                if not isinstance(context, str):
                    errors.append(
                        f"Context `{context}` in `learn_from_contexts` is not a string.")

        return errors

    def get_environment_defaults(self, environment: str) -> Dict[str, Any]:
        """
        Retrieve the default key/value pairs for a given environment.

        Parameters
        ----------
        environment : str
            The name of the environment.

        Returns
        -------
        Dict[str, Any]
            The defaults for the specified environment, or an empty dict if
            the environment is not defined.
        """
        return self.environments.get(environment, {})

    def should_learn_from_field(self, field_name: str) -> bool:
        """
        Determine whether a field should be considered for learning.

        Parameters
        ----------
        field_name : str
            The name of the field.

        Returns
        -------
        bool
            True if the field is in `learn_from_fields`, False otherwise.
        """
        return field_name in self.learn_from_fields

    def should_learn_from_context(self, context: str) -> bool:
        """
        Determine whether a context should be considered for learning.

        Parameters
        ----------
        context : str
            The context identifier.

        Returns
        -------
        bool
            True if the context is in `learn_from_contexts`, False otherwise.
        """
        return context in self.learn_from_contexts
