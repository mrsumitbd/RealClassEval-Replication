
import json
import os
from typing import Optional, Dict, Any


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
        # Assuming a simple configuration generation process for demonstration purposes
        full_config = {
            'server': {
                'host': config.get('host', 'localhost'),
                'port': config.get('port', 8080)
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'file': os.path.join(self.base_dir, config.get('log_file', 'mcp.log'))
            }
        }

        # Add other configuration sections as needed
        if 'services' in config:
            full_config['services'] = config['services']

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


# Example usage
if __name__ == "__main__":
    generator = MCPConfigGenerator()
    simplified_config = {
        'host': '0.0.0.0',
        'port': 8080,
        'log_level': 'DEBUG',
        'log_file': 'mcp_debug.log',
        'services': [
            {'name': 'service1', 'port': 8081},
            {'name': 'service2', 'port': 8082}
        ]
    }
    generator.write_config(simplified_config, 'mcp_config.json')
