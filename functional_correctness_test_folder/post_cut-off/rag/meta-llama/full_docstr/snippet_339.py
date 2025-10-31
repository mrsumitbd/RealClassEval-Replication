
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
                'port': 8080,
                'host': 'localhost'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }

        # Update the full configuration with the provided simplified config
        full_config.update(config)

        # Resolve relative paths
        for key, value in full_config.items():
            if isinstance(value, str) and value.startswith('./'):
                full_config[key] = os.path.join(self.base_dir, value[2:])

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
