from typing import TYPE_CHECKING, Any, ClassVar, TypeVar
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    project_root: Path
    json_output: bool = False
    dry_run: bool = False
    verbose: bool = False

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        return self.project_root / '.khive'

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        if hasattr(args, 'json_output'):
            self.json_output = args.json_output
        if hasattr(args, 'dry_run'):
            self.dry_run = args.dry_run
        if hasattr(args, 'verbose'):
            self.verbose = args.verbose
        global verbose_mode
        verbose_mode = self.verbose