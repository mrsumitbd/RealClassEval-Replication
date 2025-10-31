
import os
import json
from typing import Dict, Any, Optional


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir if base_dir is not None else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        generated_config = {}
        for key, value in config.items():
            if isinstance(value, str) and value.startswith('.'):
                value = os.path.join(self.base_dir, value)
            generated_config[key] = value
        return generated_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
