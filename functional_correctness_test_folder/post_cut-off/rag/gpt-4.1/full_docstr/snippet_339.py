import os
import json
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir or os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Example: expand relative paths, fill in defaults, etc.
        def resolve_path(path):
            if not path:
                return path
            if os.path.isabs(path):
                return path
            return os.path.abspath(os.path.join(self.base_dir, path))

        full_config = dict(config)  # shallow copy

        # Example: resolve paths in known keys
        path_keys = ['data_dir', 'log_dir', 'ssl_cert', 'ssl_key', 'db_path']
        for key in path_keys:
            if key in full_config:
                full_config[key] = resolve_path(full_config[key])

        # Example: fill in some defaults if not present
        defaults = {
            'host': '0.0.0.0',
            'port': 8080,
            'log_level': 'INFO',
            'workers': 4,
            'ssl_enabled': False,
        }
        for k, v in defaults.items():
            if k not in full_config:
                full_config[k] = v

        # Example: expand nested config sections if present
        if 'database' in full_config and isinstance(full_config['database'], dict):
            db = full_config['database']
            if 'path' in db:
                db['path'] = resolve_path(db['path'])
            if 'type' not in db:
                db['type'] = 'sqlite'
            full_config['database'] = db

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)
        output_path_abs = output_path
        if not os.path.isabs(output_path):
            output_path_abs = os.path.abspath(
                os.path.join(self.base_dir, output_path))
        os.makedirs(os.path.dirname(output_path_abs), exist_ok=True)
        with open(output_path_abs, 'w', encoding='utf-8') as f:
            json.dump(full_config, f, indent=2)
