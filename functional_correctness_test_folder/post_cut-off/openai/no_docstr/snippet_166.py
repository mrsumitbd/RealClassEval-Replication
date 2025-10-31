import argparse
import os
from typing import Any, Dict, Optional


class SearchAssistantConfig:
    """
    Configuration holder for the Search Assistant.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command‑line arguments.
    """

    # Define required and optional arguments with defaults
    REQUIRED_ARGS = {"index_path", "query"}
    OPTIONAL_ARGS_DEFAULTS: Dict[str, Any] = {
        "output_path": "output.txt",
        "top_k": 10,
        "device": "cpu",
    }

    def __init__(self, args: argparse.Namespace):
        # Convert Namespace to dict for easier handling
        self._args_dict: Dict[str, Any] = vars(args)

        # Set attributes for each argument
        for key, value in self._args_dict.items():
            setattr(self, key, value)

        # Apply defaults for optional arguments if not provided
        for key, default in self.OPTIONAL_ARGS_DEFAULTS.items():
            if not hasattr(self, key):
                setattr(self, key, default)

    def validate(self) -> None:
        """
        Validate the configuration.

        Raises
        ------
        ValueError
            If required arguments are missing or invalid.
        """
        # Check required arguments
        for key in self.REQUIRED_ARGS:
            if not hasattr(self, key):
                raise ValueError(f"Missing required argument: {key}")
            value = getattr(self, key)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Argument '{key}' must be a non-empty value")

        # Validate top_k
        top_k = getattr(self, "top_k", self.OPTIONAL_ARGS_DEFAULTS["top_k"])
        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("Argument 'top_k' must be a positive integer")

        # Validate device
        device = getattr(self, "device", self.OPTIONAL_ARGS_DEFAULTS["device"])
        if device not in {"cpu", "cuda"}:
            raise ValueError(
                "Argument 'device' must be either 'cpu' or 'cuda'")

        # Optional: check if index_path exists (if it refers to a file)
        index_path = getattr(self, "index_path")
        if isinstance(index_path, str) and not os.path.exists(index_path):
            raise ValueError(f"Index path does not exist: {index_path}")

        # Optional: ensure output_path is a string
        output_path = getattr(self, "output_path")
        if not isinstance(output_path, str):
            raise ValueError("Argument 'output_path' must be a string")
