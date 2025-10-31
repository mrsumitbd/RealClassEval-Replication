
import os
import json
from typing import Optional, Dict, Any


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Assuming some default configuration generation logic
        generated_config = config.copy()
        generated_config['base_dir'] = self.base_dir
        return generated_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
