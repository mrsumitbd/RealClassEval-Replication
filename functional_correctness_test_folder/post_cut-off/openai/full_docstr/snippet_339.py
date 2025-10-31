
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = Path(base_dir or os.getcwd()).resolve()

    def _resolve_path(self, value: Any) -> Any:
        """Resolve a path value relative to the base directory if it is a string."""
        if isinstance(value, str):
            p = Path(value)
            if not p.is_absolute():
                return str((self.base_dir / p).resolve())
        return value

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Start with a copy to avoid mutating the input
        full_config: Dict[str, Any] = dict(config)

        # Resolve any path-like entries
        for key, val in list(full_config.items()):
            if isinstance(val, (str, Path)):
                full_config[key] = self._resolve_path(val)
            elif isinstance(val, dict):
                full_config[key] = {k: self._resolve_path(
                    v) for k, v in val.items()}

        # Apply defaults for common MCP server settings
        defaults = {
            "server_name": "MCP Server",
            "max_players": 20,
            "motd": "Welcome to the MCP server!",
            "worlds": [],
            "plugins": [],
            "settings": {},
        }

        for k, d in defaults.items():
            full_config.setdefault(k, d)

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        out_path = Path(output_path)
        if not out_path.is_absolute():
            out_path = (self.base_dir / out_path).resolve()

        # Ensure parent directories exist
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON with pretty formatting
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, sort_keys=True)
