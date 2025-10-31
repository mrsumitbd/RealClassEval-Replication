
import os
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
        full_config = {
            'server': {
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 8080),
                'debug': config.get('debug', False)
            },
            'database': {
                'url': config.get('database_url', 'sqlite:///mcp.db'),
                'echo': config.get('database_echo', False)
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'format': config.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            },
            'auth': {
                'enabled': config.get('auth_enabled', False),
                'secret_key': config.get('auth_secret_key', 'default-secret-key'),
                'token_expiry': config.get('auth_token_expiry', 3600)
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
        abs_output_path = os.path.join(self.base_dir, output_path)
        os.makedirs(os.path.dirname(abs_output_path), exist_ok=True)
        with open(abs_output_path, 'w') as f:
            import json
            json.dump(full_config, f, indent=4)
