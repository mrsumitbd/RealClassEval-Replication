
import json
import os
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    """
    A simple configuration generator for MCP (Multi‑Channel Processor) projects.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the generator with an optional base directory.
        If base_dir is None, the current working directory is used.
        """
        self.base_dir = os.path.abspath(base_dir) if base_dir else os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge the supplied configuration with a set of defaults.
        The supplied config overrides the defaults.
        """
        defaults: Dict[str, Any] = {
            "mcp_version": "1.0",
            "channels": [],
            "logging": {
                "level": "INFO",
                "file": "mcp.log",
            },
            "output_dir": os.path.join(self.base_dir, "output"),
        }

        # Deep merge for nested dictionaries
        def deep_merge(dflt: Dict[str, Any], upd: Dict[str, Any]) -> Dict[str, Any]:
            result = dict(dflt)
            for key, val in upd.items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(val, dict)
                ):
                    result[key] = deep_merge(result[key], val)
                else:
                    result[key] = val
            return result

        merged = deep_merge(defaults, config)
        return merged

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        """
        Write the configuration dictionary to a JSON file.
        The output_path can be relative to the base_dir.
        """
        # Resolve the full path
        full_path = (
            os.path.join(self.base_dir, output_path)
            if not os.path.isabs(output_path)
            else output_path
        )
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, sort_keys=True)
