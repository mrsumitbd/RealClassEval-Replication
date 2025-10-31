import os
import json
from typing import Optional, Dict, Any


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

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
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Deep copy to avoid mutating input
        import copy
        cfg = copy.deepcopy(config)

        # Example: fill in defaults for missing keys
        defaults = {
            "server": {
                "host": "0.0.0.0",
                "port": 8080,
                "log_level": "info"
            },
            "database": {
                "type": "sqlite",
                "path": "mcp.db"
            },
            "auth": {
                "enabled": False
            }
        }

        def merge(d, default):
            for k, v in default.items():
                if k not in d:
                    d[k] = v
                elif isinstance(v, dict) and isinstance(d[k], dict):
                    merge(d[k], v)
            return d

        cfg = merge(cfg, defaults)

        # Resolve relative paths in database config
        db = cfg.get("database", {})
        if db.get("type") == "sqlite" and "path" in db:
            db_path = db["path"]
            if not os.path.isabs(db_path):
                db["path"] = os.path.abspath(
                    os.path.join(self.base_dir, db_path))
            cfg["database"] = db

        # Add any other required transformations here

        return cfg

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)
        output_path_abs = output_path
        if not os.path.isabs(output_path):
            output_path_abs = os.path.abspath(
                os.path.join(self.base_dir, output_path))
        with open(output_path_abs, "w", encoding="utf-8") as f:
            json.dump(full_config, f, indent=2)
