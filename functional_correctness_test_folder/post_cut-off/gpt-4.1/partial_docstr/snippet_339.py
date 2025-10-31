
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
        if base_dir is None:
            self.base_dir = os.getcwd()
        else:
            self.base_dir = os.path.abspath(base_dir)

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        def resolve_path(path):
            if not isinstance(path, str):
                return path
            if os.path.isabs(path):
                return path
            return os.path.abspath(os.path.join(self.base_dir, path))

        def process_dict(d):
            result = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    result[k] = process_dict(v)
                elif isinstance(v, list):
                    result[k] = [process_dict(i) if isinstance(i, dict) else resolve_path(i) if isinstance(
                        i, str) and (k.endswith('_path') or k.endswith('_file') or k.endswith('_dir')) else i for i in v]
                elif isinstance(v, str) and (k.endswith('_path') or k.endswith('_file') or k.endswith('_dir')):
                    result[k] = resolve_path(v)
                else:
                    result[k] = v
            return result

        return process_dict(config)

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        output_path = os.path.abspath(os.path.join(self.base_dir, output_path))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
