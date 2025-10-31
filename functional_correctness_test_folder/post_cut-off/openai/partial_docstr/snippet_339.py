
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union


class MCPConfigGenerator:
    """
    A simple configuration generator that resolves relative paths
    against a base directory and writes the resulting configuration
    to a JSON file.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the MCP config generator.

        Args:
            base_dir: Base directory for resolving relative paths
                      (defaults to the current working directory).
        """
        self.base_dir = Path(base_dir or os.getcwd()).resolve()

    def _resolve_path(self, value: str) -> str:
        """
        Resolve a string that looks like a file path relative to the base directory.
        If the string is already an absolute path or does not look like a path,
        it is returned unchanged.

        Args:
            value: The string to potentially resolve.

        Returns:
            The resolved absolute path as a string.
        """
        # Heuristic: treat as a path if it contains a slash or backslash
        if "/" in value or "\\" in value:
            p = Path(value)
            if not p.is_absolute():
                p = (self.base_dir / p).resolve()
            return str(p)
        return value

    def _process_value(self, value: Any) -> Any:
        """
        Recursively process a value, resolving paths where appropriate.

        Args:
            value: The value to process.

        Returns:
            The processed value.
        """
        if isinstance(value, dict):
            return {k: self._process_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._process_value(v) for v in value]
        if isinstance(value, str):
            return self._resolve_path(value)
        return value

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a simplified configuration dictionary by resolving
        relative paths against the base directory.

        Args:
            config: The original configuration dictionary.

        Returns:
            A new dictionary with resolved paths.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        return self._process_value(config)

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        """
        Write the generated configuration to a file in JSON format.

        Args:
            config: The simplified configuration dictionary.
            output_path: Path to write the generated configuration.
        """
        out_path = Path(output_path).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, sort_keys=True)
