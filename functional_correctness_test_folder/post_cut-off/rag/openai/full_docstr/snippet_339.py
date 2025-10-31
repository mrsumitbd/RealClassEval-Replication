
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
        self.base_dir = Path(base_dir or Path.cwd()).resolve()

    def _resolve_path(self, value: Any) -> Any:
        """
        Resolve a path value relative to the base directory.
        If the value is a string that represents a path and is not absolute,
        it will be joined with the base directory.
        """
        if isinstance(value, str):
            p = Path(value)
            if not p.is_absolute():
                return str((self.base_dir / p).resolve())
        return value

    def _merge_dicts(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries.
        Values from `override` take precedence over those in `base`.
        """
        result = dict(base)
        for key, val in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(val, dict)
            ):
                result[key] = self._merge_dicts(result[key], val)
            else:
                result[key] = val
        return result

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Default configuration
        default_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8080,
                "workers": 4,
            },
            "logging": {
                "level": "INFO",
                "file": "mcp.log",
            },
            "paths": {
                "data_dir": str(self.base_dir / "data"),
                "log_dir": str(self.base_dir / "logs"),
            },
            "features": {
                "enable_auth": False,
                "max_connections": 1000,
            },
        }

        # Resolve any relative paths in the user config
        resolved_user_config = {}
        for k, v in config.items():
            if isinstance(v, dict):
                resolved_user_config[k] = {
                    sub_k: self._resolve_path(sub_v)
                    for sub_k, sub_v in v.items()
                }
            else:
                resolved_user_config[k] = self._resolve_path(v)

        # Merge user config over defaults
        full_config = self._merge_dicts(default_config, resolved_user_config)

        # Ensure all path values are absolute strings
        if "paths" in full_config:
            for key, path in full_config["paths"].items():
                full_config["paths"][key] = str(Path(path).resolve())

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)
        out_path = Path(output_path).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(full_config, f, indent=2, sort_keys=True)
