
import logging
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        if not server_name:
            raise MissingArgumentError("server_name cannot be an empty string")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(f"Error validating server {server_name}: {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        servers_base_path = app_context.settings.get('paths.servers')
        if not servers_base_path:
            raise AppFileNotFoundError(
                "Main server base directory is not configured")

        servers_path = Path(servers_base_path)
        if not servers_path.exists():
            raise AppFileNotFoundError(
                f"Main server base directory {servers_path} does not exist")

        servers_data = []
        errors = []

        for server_dir in servers_path.iterdir():
            if server_dir.is_dir():
                server_name = server_dir.name
                try:
                    server = BedrockServer(server_name, app_context)
                    if server.is_installed():
                        status = server.get_status()
                        version = server.get_version()
                        servers_data.append({
                            "name": server_name,
                            "status": status,
                            "version": version
                        })
                except Exception as e:
                    errors.append(
                        f"Error processing server {server_name}: {e}")

        servers_data.sort(key=lambda x: x["name"])
        return servers_data, errors
