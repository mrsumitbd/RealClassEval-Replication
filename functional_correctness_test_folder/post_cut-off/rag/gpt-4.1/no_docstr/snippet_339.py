import os
import json
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = base_dir or os.getcwd()

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Start with a default skeleton
        full_config = {
            "server": {
                "host": config.get("host", "0.0.0.0"),
                "port": config.get("port", 8080),
                "log_level": config.get("log_level", "info"),
                "ssl": config.get("ssl", None)
            },
            "database": {
                "type": config.get("db_type", "sqlite"),
                "uri": config.get("db_uri", "sqlite:///mcp.db"),
                "pool_size": config.get("db_pool_size", 5)
            },
            "auth": {
                "enabled": config.get("auth_enabled", False),
                "providers": config.get("auth_providers", [])
            },
            "plugins": config.get("plugins", []),
            "storage": {
                "root": self._resolve_path(config.get("storage_root", "./storage")),
                "max_size_mb": config.get("storage_max_size_mb", 10240)
            }
        }
        # Merge/override with any extra keys in config
        for k, v in config.items():
            if k not in ["host", "port", "log_level", "ssl", "db_type", "db_uri", "db_pool_size", "auth_enabled", "auth_providers", "plugins", "storage_root", "storage_max_size_mb"]:
                full_config[k] = v
        return full_config

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_config = self.generate_config(config)
        output_path = self._resolve_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(full_config, f, indent=2)

    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(self.base_dir, path))
