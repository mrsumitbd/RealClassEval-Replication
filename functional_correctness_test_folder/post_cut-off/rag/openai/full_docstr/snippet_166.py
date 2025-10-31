
import argparse
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    # List of parameters that are considered mandatory for a typical
    # search‑assistant invocation.  The names are chosen to match the
    # most common CLI flags used in the project.  If the project
    # evolves, simply add or remove names from this list.
    _REQUIRED_PARAMS: List[str] = [
        "model_id",
        "query",
    ]

    # Optional parameters that have a natural type and a sensible
    # default value.  The dictionary maps the attribute name to a
    # tuple of (expected type, default value).
    _OPTIONAL_PARAMS: Dict[str, Any] = {
        "max_results": (int, 10),
        "temperature": (float, 0.7),
        "top_k": (int, 50),
        "output_file": (str, None),
        "verbose": (bool, False),
    }

    def __init__(self, args: argparse.Namespace):
        """
        Initialize configuration from command line arguments.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments.
        """
        if not isinstance(args, argparse.Namespace):
            raise TypeError("args must be an argparse.Namespace instance")

        # Store the raw namespace for reference
        self._raw_args = args

        # Populate attributes from the namespace
        for key, value in vars(args).items():
            setattr(self, key, value)

        # Ensure all optional parameters are present (even if not supplied)
        for key, (typ, default) in self._OPTIONAL_PARAMS.items():
            if not hasattr(self, key):
                setattr(self, key, default)

    def validate(self) -> None:
        """
        Validate configuration parameters.

        Raises
        ------
        ValueError
            If any configuration parameter is invalid.
        """
        # 1. Check required parameters
        missing = [p for p in self._REQUIRED_PARAMS if getattr(
            self, p, None) is None]
        if missing:
            raise ValueError(
                f"Missing required configuration parameters: {', '.join(missing)}")

        # 2. Validate optional parameters that have type constraints
        for key, (typ, _) in self._OPTIONAL_PARAMS.items():
            value = getattr(self, key, None)
            if value is None:
                continue  # optional and not supplied
            if not isinstance(value, typ):
                raise ValueError(
                    f"Parameter '{key}' must be of type {typ.__name__}")

            # Additional semantic checks
            if key == "max_results" and value <= 0:
                raise ValueError("max_results must be a positive integer")
            if key == "top_k" and value <= 0:
                raise ValueError("top_k must be a positive integer")
            if key == "temperature":
                if not (0.0 <= value <= 1.0):
                    raise ValueError(
                        "temperature must be between 0.0 and 1.0 inclusive")

        # 3. Validate output file path if supplied
        output_file: Optional[str] = getattr(self, "output_file", None)
        if output_file:
            path = Path(output_file)
            if path.is_dir():
                raise ValueError(f"output_file '{output_file}' is a directory")
            # Ensure parent directory exists (create if necessary)
            if not path.parent.exists():
                try:
                    path.parent.mkdir(parents=True, exist_ok=True)
                except Exception as exc:
                    raise ValueError(
                        f"Cannot create directory for output_file: {exc}") from exc

        # 4. Validate model_id format (basic sanity check)
        model_id: str = getattr(self, "model_id")
        if not isinstance(model_id, str) or not model_id.strip():
            raise ValueError("model_id must be a non‑empty string")

        # 5. Validate query string
        query: str = getattr(self, "query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non‑empty string")

        # 6. Validate verbose flag
        verbose: bool = getattr(self, "verbose")
        if not isinstance(verbose, bool):
            raise ValueError("verbose must be a boolean")

        # All checks passed
        return None
