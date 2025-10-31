
from typing import Optional, Dict, Any
import json
import os


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir if base_dir is not None else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(config, dict):
            raise ValueError("Input config must be a dictionary")
        return config.copy()

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        full_path = os.path.join(self.base_dir, output_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            json.dump(config, f, indent=4)
