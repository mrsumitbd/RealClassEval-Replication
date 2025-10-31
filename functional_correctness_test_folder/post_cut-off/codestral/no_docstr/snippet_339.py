
import os
import json
from typing import Dict, Any, Optional


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):

        self.base_dir = base_dir

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:

        if self.base_dir is not None:
            config['base_dir'] = self.base_dir
        return config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=4)
