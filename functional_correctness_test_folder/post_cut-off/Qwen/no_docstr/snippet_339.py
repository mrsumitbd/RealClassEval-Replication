
from typing import Optional, Dict, Any
import os
import json


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Example implementation: Add a default version if not provided
        if 'version' not in config:
            config['version'] = '1.0'
        return config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        if self.base_dir:
            output_path = os.path.join(self.base_dir, output_path)
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
