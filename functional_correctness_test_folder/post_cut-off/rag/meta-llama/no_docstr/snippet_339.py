
import json
import os
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    """Generator for MCP server configuration."""

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the MCP config generator.

        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        """
        self.base_dir = base_dir if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a full MCP server configuration from a simplified config.

        Args:
            config: Simplified configuration dictionary

        Returns:
            Complete MCP server configuration
        """
        # Assuming some default configuration structure
        full_config = {
            'server': {
                'port': config.get('port', 8080),
                'host': config.get('host', 'localhost')
            },
            'logging': {
                'level': config.get('log_level', 'INFO'),
                'file': config.get('log_file', 'mcp.log')
            },
            # Add other configuration sections as needed
        }

        # Resolve relative paths
        if 'logging' in full_config and 'file' in full_config['logging']:
            log_file = full_config['logging']['file']
            if not os.path.isabs(log_file):
                full_config['logging']['file'] = os.path.join(
                    self.base_dir, log_file)

        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        """
        Write the generated configuration to a file.

        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        """
        full_config = self.generate_config(config)
        with open(output_path, 'w') as f:
            json.dump(full_config, f, indent=4)
