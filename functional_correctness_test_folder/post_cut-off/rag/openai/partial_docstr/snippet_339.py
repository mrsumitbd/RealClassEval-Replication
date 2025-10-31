
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
        """
        Resolve a path value relative to the base directory if it is a string
        and not an absolute path. Non-string values are returned unchanged.
        """
        if isinstance(value, str):
            path = Path(value)
            if not path.is_absolute():
                return str((self.base_dir / path).resolve())
        return value

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Start with a copy to avoid mutating the caller's dict
        full_config: Dict[str, Any] = dict(config)

        # Resolve any path-like entries
        for key, val in list(full_config.items()):
            if key.endswith(('_path', '_dir', '_file', '_folder')):
                full_config[key] = self._resolve_path(val)

        # Add defaults for missing top‑level keys
        defaults = {
            'host': '0.0.0.0',
            'port': 8080,
            'debug': False,
            'log_level': 'INFO',
            'max_connections': 100,
            'timeout_seconds': 30,
        }
        for k, v in defaults.items():
            full_config.setdefault(k, v)

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

        with out_path.open('w', encoding='utf-8') as f:
            json.dump(full_config, f, indent=2, sort_keys=True)
