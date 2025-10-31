
import os
import json
from typing import Optional, Dict, Any


class MCPConfigGenerator:

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        generated = dict(config)
        if self.base_dir:
            generated['base_dir'] = self.base_dir
        generated['generated'] = True
        return generated

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        if self.base_dir and not os.path.isabs(output_path):
            output_path = os.path.join(self.base_dir, output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
