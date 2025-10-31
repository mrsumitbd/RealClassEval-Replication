from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
import os


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    config_dir: Optional[Path] = None
    config_file: Optional[Path] = None
    log_level: Optional[str] = None
    verbose: bool = False
    quiet: bool = False
    color: Optional[bool] = None
    dry_run: bool = False
    profile: Optional[str] = None

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        if self.config_dir:
            return Path(self.config_dir).expanduser().resolve()
        env_dir = os.getenv("KHIVE_CONFIG_DIR") or os.getenv("KHIVE_HOME")
        if env_dir:
            return Path(env_dir).expanduser().resolve()
        xdg = os.getenv("XDG_CONFIG_HOME")
        if xdg:
            return (Path(xdg).expanduser().resolve() / "khive")
        return Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        def get_arg(name: str, default: Any = None) -> Any:
            if isinstance(args, dict):
                return args.get(name, default)
            return getattr(args, name, default)

        cfg_dir = get_arg("config_dir", None)
        if cfg_dir is not None:
            self.config_dir = Path(cfg_dir) if not isinstance(
                cfg_dir, Path) else cfg_dir

        cfg_file = get_arg("config_file", None) or get_arg("config", None)
        if cfg_file is not None:
            self.config_file = Path(cfg_file) if not isinstance(
                cfg_file, Path) else cfg_file

        verbose = get_arg("verbose", None)
        if verbose is not None:
            self.verbose = bool(verbose)

        quiet = get_arg("quiet", None)
        if quiet is not None:
            self.quiet = bool(quiet)
            if self.quiet:
                self.verbose = False

        color = get_arg("color", None)
        if color is None:
            no_color = get_arg("no_color", None)
            if no_color is not None:
                color = not bool(no_color)
        if color is not None:
            self.color = bool(color)

        dry = get_arg("dry_run", None) or get_arg("dry", None)
        if dry is not None:
            self.dry_run = bool(dry)

        prof = get_arg("profile", None)
        if prof is not None:
            self.profile = str(prof)

        level = get_arg("log_level", None) or get_arg(
            "loglevel", None) or get_arg("log", None)
        debug = get_arg("debug", None)
        if level is not None:
            self.log_level = str(level).upper()
        elif debug is not None:
            if debug:
                self.log_level = "DEBUG"
        else:
            if self.log_level is None:
                if self.quiet:
                    self.log_level = "ERROR"
                elif self.verbose:
                    self.log_level = "DEBUG"
                else:
                    self.log_level = "INFO"
