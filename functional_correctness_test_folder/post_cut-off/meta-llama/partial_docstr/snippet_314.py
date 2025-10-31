
import logging
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path

# Assuming the following imports are available
from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError
from .app_context import AppContext
from . import settings


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        if not server_name:
            raise MissingArgumentError("Server name cannot be empty")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(f"Error validating server {server_name}: {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        servers_base_dir = Path(settings['paths.servers'])
        if not servers_base_dir.exists() or not servers_base_dir.is_dir():
            raise AppFileNotFoundError(
                f"Main server base directory '{servers_base_dir}' does not exist or is not a directory")

        server_data = []
        error_messages = []

        for server_dir in servers_base_dir.iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir.name, app_context)
                    if server.is_installed():
                        status = server.get_status()
                        version = server.get_version()
                        server_data.append({
                            "name": server_dir.name,
                            "status": status,
                            "version": version
                        })
                except Exception as e:
                    error_messages.append(
                        f"Error processing server {server_dir.name}: {e}")

        server_data.sort(key=lambda x: x['name'])
        return server_data, error_messages
