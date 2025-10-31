
import os
import json
from typing import Optional, Dict, Any


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Assuming a simple configuration transformation for demonstration purposes
        generated_config = {}
        for key, value in config.items():
            if isinstance(value, dict):
                generated_config[key] = self.generate_config(value)
            else:
                generated_config[key] = value
        return generated_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)


# Example usage
if __name__ == "__main__":
    generator = MCPConfigGenerator()
    config = {
        "key1": "value1",
        "key2": {
            "nested_key1": "nested_value1",
            "nested_key2": "nested_value2"
        }
    }
    generated_config = generator.generate_config(config)
    generator.write_config(generated_config, 'output/config.json')
