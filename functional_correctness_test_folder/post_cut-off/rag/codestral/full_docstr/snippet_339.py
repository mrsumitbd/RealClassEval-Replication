
import os
import json
from typing import Dict, Any, Optional


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir if base_dir is not None else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Default configuration structure
        full_config = {
            'server': {
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 8080),
                'workers': config.get('workers', 4),
                'timeout': config.get('timeout', 30),
                'debug': config.get('debug', False)
            },
            'database': {
                'type': config.get('db_type', 'sqlite'),
                'connection': config.get('db_connection', 'mcp.db'),
                'pool_size': config.get('db_pool_size', 10)
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'file': config.get('log_file', 'mcp.log'),
                'max_size': config.get('log_max_size', 10485760),
                'backup_count': config.get('log_backup_count', 5)
            },
            'security': {
                'ssl': config.get('ssl', False),
                'cert_file': config.get('cert_file', None),
                'key_file': config.get('key_file', None),
                'cors': config.get('cors', False),
                'allowed_origins': config.get('allowed_origins', ['*'])
            }
        }

        # Resolve relative paths
        if full_config['logging']['file'] and not os.path.isabs(full_config['logging']['file']):
            full_config['logging']['file'] = os.path.join(
                self.base_dir, full_config['logging']['file'])

        if full_config['security']['cert_file'] and not os.path.isabs(full_config['security']['cert_file']):
            full_config['security']['cert_file'] = os.path.join(
                self.base_dir, full_config['security']['cert_file'])

        if full_config['security']['key_file'] and not os.path.isabs(full_config['security']['key_file']):
            full_config['security']['key_file'] = os.path.join(
                self.base_dir, full_config['security']['key_file'])

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write to file
        with open(output_path, 'w') as f:
            json.dump(full_config, f, indent=4)
