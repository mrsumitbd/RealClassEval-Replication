
import argparse
import os
from pathlib import Path


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        if not isinstance(args, argparse.Namespace):
            raise TypeError("args must be an argparse.Namespace instance")

        # Store raw args for reference
        self._args = args

        # Extract expected configuration options with sensible defaults
        self.model_name: str | None = getattr(args, "model", None)
        self.query: str | None = getattr(args, "query", None)
        self.max_results: int = getattr(args, "max_results", 10)
        self.threshold: float = getattr(args, "threshold", 0.5)
        self.output_file: str | None = getattr(args, "output", None)
        self.verbose: bool = getattr(args, "verbose", False)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        # Basic type checks
        if self.model_name is None or not isinstance(self.model_name, str):
            raise ValueError("model name must be a non-empty string")

        if self.query is None or not isinstance(self.query, str):
            raise ValueError("query must be a non-empty string")

        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        if not isinstance(self.threshold, (float, int)) or not (0.0 <= self.threshold <= 1.0):
            raise ValueError("threshold must be a float between 0 and 1")

        # Validate output file path if provided
        if self.output_file:
            out_path = Path(self.output_file)
            if out_path.is_dir():
                raise ValueError(
                    f"output path '{self.output_file}' is a directory")
            parent = out_path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                except Exception as exc:
                    raise ValueError(
                        f"cannot create directory for output file: {exc}") from exc
            # Check write permission
            try:
                with out_path.open("a"):
                    pass
            except Exception as exc:
                raise ValueError(
                    f"cannot write to output file '{self.output_file}': {exc}") from exc
