
import argparse
import json
import pathlib
from typing import Any, Optional


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """
        Initialize configuration from command line arguments.

        Args:
            args: Parsed command line arguments.
        """
        self.args: argparse.Namespace = args

        # Basic required parameters
        self.model_name: Optional[str] = getattr(args, "model_name", None)
        self.query: Optional[str] = getattr(args, "query", None)

        # Optional parameters with defaults
        self.max_results: int = getattr(args, "max_results", 10)
        self.threshold: float = getattr(args, "threshold", 0.5)
        self.verbose: bool = getattr(args, "verbose", False)
        self.output_file: Optional[str] = getattr(args, "output_file", None)

        # Load additional configuration from a JSON file if provided
        config_file: Optional[str] = getattr(args, "config_file", None)
        if config_file:
            config_path = pathlib.Path(config_file)
            if not config_path.is_file():
                raise ValueError(
                    f"Config file '{config_file}' does not exist.")
            with config_path.open("r", encoding="utf-8") as f:
                cfg: dict[str, Any] = json.load(f)
            for key, value in cfg.items():
                setattr(self, key, value)

    def validate(self) -> None:
        """
        Validate configuration parameters.

        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        # Validate required string parameters
        if not self.model_name or not isinstance(self.model_name, str):
            raise ValueError("`model_name` must be a non‑empty string.")
        if not self.query or not isinstance(self.query, str):
            raise ValueError("`query` must be a non‑empty string.")

        # Validate numeric parameters
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("`max_results` must be a positive integer.")
        if not isinstance(self.threshold, (float, int)) or not (0 <= self.threshold <= 1):
            raise ValueError(
                "`threshold` must be a float between 0 and 1 inclusive.")

        # Validate boolean flag
        if not isinstance(self.verbose, bool):
            raise ValueError("`verbose` must be a boolean value.")

        # Validate output file path if provided
        if self.output_file:
            out_path = pathlib.Path(self.output_file)
            if out_path.is_dir():
                raise ValueError("`output_file` cannot be a directory.")
