
from typing import Optional, Dict, Any
import os
import json


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Example implementation: Add a version key to the config
        config['version'] = '1.0'
        return config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        if not os.path.isabs(output_path):
            output_path = os.path.join(self.base_dir, output_path)
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
