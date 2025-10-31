
import os
from typing import Optional, Dict, Any
import json


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
        full_config = {
            'version': '1.0',
            'settings': {
                'debug': config.get('debug', False),
                'log_level': config.get('log_level', 'info'),
                'max_connections': config.get('max_connections', 100),
            },
            'services': config.get('services', []),
            'paths': {
                'base': os.path.abspath(os.path.join(self.base_dir, config.get('base_path', ''))),
                'logs': os.path.abspath(os.path.join(self.base_dir, config.get('log_path', 'logs'))),
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
