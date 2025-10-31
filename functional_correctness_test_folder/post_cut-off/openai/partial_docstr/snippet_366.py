
from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    """
    Base configuration class for khive projects.

    Sub‑classes should declare dataclass fields that represent
    configuration options.  The :py:meth:`update_from_cli_args` method
    will automatically copy values from a namespace (e.g. the result
    of ``argparse.ArgumentParser.parse_args``) into the corresponding
    fields of the configuration instance.
    """

    @property
    def khive_config_dir(self) -> Path:
        """
        Return the absolute path to the ``.khive`` configuration directory.

        The directory is located in the current user's home directory
        and is named ``.khive``.  The directory is created lazily by
        callers that need it; this property only resolves the path.
        """
        return Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        """
        Update configuration fields from a CLI arguments namespace.

        Parameters
        ----------
        args : Any
            An object that provides attribute access to CLI arguments
            (typically the namespace returned by ``argparse``).  If an
            attribute with the same name as a dataclass field exists
            and its value is not ``None``, the field is updated with
            that value.

        Notes
        -----
        The method is intentionally tolerant: if ``args`` does not
        provide an attribute for a field, the field is left unchanged.
        """
        for field_def in fields(self):
            if hasattr(args, field_def.name):
                value = getattr(args, field_def.name)
                if value is not None:
                    setattr(self, field_def.name, value)
