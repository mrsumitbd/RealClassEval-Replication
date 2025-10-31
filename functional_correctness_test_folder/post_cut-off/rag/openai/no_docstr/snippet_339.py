
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
        """Resolve a path value relative to the base directory."""
        if isinstance(value, str):
            p = Path(value)
            if not p.is_absolute():
                return str((self.base_dir / p).resolve())
        return value

    def _resolve_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively resolve all string paths in a dictionary."""
        resolved = {}
        for k, v in d.items():
            if isinstance(v, dict):
                resolved[k] = self._resolve_dict(v)
            elif isinstance(v, list):
                resolved[k] = [self._resolve_path(item) for item in v]
            else:
                resolved[k] = self._resolve_path(v)
        return resolved

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Start with a copy to avoid mutating the input
        full_config = dict(config)

        # Resolve relative paths
        full_config = self._resolve_dict(full_config)

        # Add default server section if missing
        server_cfg = full_config.get('server', {})
        server_cfg.setdefault('host', '0.0.0.0')
        server_cfg.setdefault('port', 8080)
        full_config['server'] = server_cfg

        # Add default logging section if missing
        logging_cfg = full_config.get('logging', {})
        logging_cfg.setdefault('level', 'INFO')
        logging_cfg.setdefault('file', str(self.base_dir / 'mcp.log'))
        full_config['logging'] = logging_cfg

        # Ensure any nested config sections are also resolved
        for key in ['database', 'storage', 'auth']:
            if key in full_config and isinstance(full_config[key], dict):
                full_config[key] = self._resolve_dict(full_config[key])

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        output_file = Path(output_path).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, sort_keys=True)
