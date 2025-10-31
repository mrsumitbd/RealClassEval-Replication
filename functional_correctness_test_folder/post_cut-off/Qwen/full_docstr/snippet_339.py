
from typing import Optional, Dict, Any
import os
import json


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Example transformation: expand paths relative to base_dir
        full_config = {
            'server': {
                'host': config.get('host', 'localhost'),
                'port': config.get('port', 8080),
                'data_dir': os.path.join(self.base_dir, config.get('data_dir', 'data')),
                'log_dir': os.path.join(self.base_dir, config.get('log_dir', 'logs')),
            },
            'features': config.get('features', {}),
            'security': {
                'enabled': config.get('security', {}).get('enabled', False),
                'api_key': config.get('security', {}).get('api_key', None),
            }
        }
        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)
        with open(output_path, 'w') as f:
            json.dump(full_config, f, indent=4)
