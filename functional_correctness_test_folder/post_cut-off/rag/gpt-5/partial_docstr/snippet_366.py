from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
import os


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    # Optional override of the configuration directory, typically set via CLI
    config_dir: Optional[Path] = None

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        if self.config_dir is not None:
            path = Path(self.config_dir).expanduser()
        else:
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config:
                path = Path(xdg_config).expanduser() / "khive"
            else:
                path = Path.home() / ".khive"

        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Silently ignore directory creation issues; consumer can handle missing dir
            pass
        return path

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        if args is None:
            return

        if isinstance(args, dict):
            items = args.items()
        else:
            try:
                items = vars(args).items()
            except TypeError:
                items = (
                    (k, getattr(args, k))
                    for k in dir(args)
                    if not k.startswith("_") and not callable(getattr(args, k))
                )

        for key, value in items:
            if value is None:
                continue
            attr = key.replace("-", "_")

            # Special handling for config directory overrides
            if attr in {"config_dir", "khive_config_dir"}:
                self.config_dir = Path(value).expanduser()
                continue

            # Only set attributes that exist on the dataclass
            if hasattr(self, attr):
                setattr(self, attr, value)
