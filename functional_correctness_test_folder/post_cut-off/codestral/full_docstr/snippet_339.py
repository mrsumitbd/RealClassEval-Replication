
import os
from typing import Dict, Any, Optional
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
            'server': {
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 8080),
                'workers': config.get('workers', 4),
                'timeout': config.get('timeout', 30),
                'debug': config.get('debug', False)
            },
            'database': {
                'host': config.get('db_host', 'localhost'),
                'port': config.get('db_port', 5432),
                'name': config.get('db_name', 'mcp'),
                'user': config.get('db_user', 'mcp_user'),
                'password': config.get('db_password', 'mcp_password')
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'file': os.path.join(self.base_dir, config.get('log_file', 'mcp.log'))
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
