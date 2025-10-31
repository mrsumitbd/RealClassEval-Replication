
from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, get_type_hints
import os


@dataclass
class BaseConfig:
    """
    Base configuration class for khive.

    Subclasses should declare dataclass fields that represent configuration
    options.  The class provides a convenient property to locate the
    configuration directory and a helper to update configuration values
    from parsed CLI arguments.
    """

    @property
    def khive_config_dir(self) -> Path:
        """
        Return the path to the khive configuration directory.

        The directory is determined in the following order:

        1. If the environment variable ``KHIIVE_CONFIG_DIR`` is set,
           its value is used.
        2. Otherwise, ``~/.khive`` is used.

        The returned path is guaranteed to be a :class:`pathlib.Path`
        instance.
        """
        env_dir = os.getenv("KHIIVE_CONFIG_DIR")
        if env_dir:
            return Path(env_dir).expanduser().resolve()
        return Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        """
        Update configuration fields from a namespace of CLI arguments.

        Parameters
        ----------
        args : Any
            An object (typically a ``argparse.Namespace``) that may contain
            attributes matching the names of the dataclass fields.  For each
            field that exists on ``args``, the corresponding attribute on
            ``self`` is updated.  If the field type is annotated, an attempt
            is made to cast the value to that type.

        Notes
        -----
        - Only fields defined on the dataclass are considered.
        - If a field is missing from ``args`` it is left unchanged.
        - If a field is present but the value cannot be cast to the annotated
          type, a ``ValueError`` is raised.
        """
        # Retrieve type hints for casting
        type_hints = get_type_hints(self.__class__)
        for f in fields(self):
            if hasattr(args, f.name):
                raw_value = getattr(args, f.name)
                # Cast to the annotated type if available
                target_type = type_hints.get(f.name, type(raw_value))
                try:
                    # Handle special case for bool: argparse may provide
                    # strings like "True"/"False" or actual bools.
                    if target_type is bool and isinstance(raw_value, str):
                        cast_value = raw_value.lower() in ("1", "true", "yes", "on")
                    else:
                        cast_value = target_type(raw_value)
                except Exception as exc:
                    raise ValueError(
                        f"Failed to cast CLI argument '{f.name}' "
                        f"to {target_type.__name__}: {exc}"
                    ) from exc
                setattr(self, f.name, cast_value)
