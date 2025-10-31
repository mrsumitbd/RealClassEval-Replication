
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
        self.base_dir = base_dir or os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        full_config = {
            'server': {
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 8080),
                'debug': config.get('debug', False)
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'file': os.path.join(self.base_dir, config.get('log_file', 'mcp.log'))
            },
            'database': {
                'type': config.get('db_type', 'sqlite'),
                'connection_string': config.get('db_connection_string', 'sqlite:///mcp.db')
            },
            'features': {
                'feature1': config.get('feature1', True),
                'feature2': config.get('feature2', False)
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
