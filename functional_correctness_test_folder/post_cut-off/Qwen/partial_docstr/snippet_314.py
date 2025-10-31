
from typing import Optional, List, Dict, Any, Tuple
import os
import logging
from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        if not server_name:
            raise MissingArgumentError(
                "server_name cannot be an empty string.")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(f"Error validating server {server_name}: {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        if app_context is None:
            raise MissingArgumentError("app_context cannot be None.")

        servers_base_dir = app_context.settings.get('paths', {}).get('servers')
        if not servers_base_dir or not os.path.isdir(servers_base_dir):
            raise AppFileNotFoundError(
                f"Server base directory not found: {servers_base_dir}")

        server_data = []
        errors = []

        for server_name in os.listdir(servers_base_dir):
            server_path = os.path.join(servers_base_dir, server_name)
            if os.path.isdir(server_path):
                try:
                    server = BedrockServer(server_name, app_context)
                    if server.is_installed():
                        status = server.get_status()
                        version = server.get_version()
                        server_data.append({
                            "name": server_name,
                            "status": status,
                            "version": version
                        })
                except Exception as e:
                    errors.append(
                        f"Error processing server {server_name}: {e}")

        server_data.sort(key=lambda x: x['name'])
        return server_data, errors
