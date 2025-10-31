
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

    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(self.base_dir, path))

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        # Start with a default template
        full_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 25565,
                "motd": "A Minecraft Server",
                "max_players": 20,
                "online_mode": True,
                "level_name": "world",
                "level_seed": "",
                "white_list": False,
                "enable_command_block": False,
                "view_distance": 10,
                "resource_pack": "",
                "resource_pack_sha1": "",
                "plugins": [],
                "properties": {}
            },
            "logging": {
                "level": "INFO",
                "file": "logs/server.log"
            }
        }

        # Update server section
        server_conf = config.get("server", {})
        for key in full_config["server"]:
            if key in server_conf:
                full_config["server"][key] = server_conf[key]

        # Resolve paths for level_name, resource_pack, and plugins if present
        if "level_name" in full_config["server"]:
            full_config["server"]["level_name"] = self._resolve_path(
                str(full_config["server"]["level_name"]))
        if full_config["server"].get("resource_pack"):
            full_config["server"]["resource_pack"] = self._resolve_path(
                str(full_config["server"]["resource_pack"]))
        if full_config["server"].get("plugins"):
            full_config["server"]["plugins"] = [
                self._resolve_path(str(p)) for p in full_config["server"]["plugins"]
            ]

        # Merge properties if provided
        if "properties" in server_conf:
            full_config["server"]["properties"].update(
                server_conf["properties"])

        # Update logging section
        logging_conf = config.get("logging", {})
        for key in full_config["logging"]:
            if key in logging_conf:
                full_config["logging"][key] = logging_conf[key]
        # Resolve log file path
        if "file" in full_config["logging"]:
            full_config["logging"]["file"] = self._resolve_path(
                str(full_config["logging"]["file"]))

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
            json.dump(full_config, f, indent=4)
