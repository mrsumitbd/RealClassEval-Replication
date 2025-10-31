
from typing import Optional, List, Dict, Any, Tuple
from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError
import os
import logging


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        if not server_name:
            raise MissingArgumentError("server_name cannot be an empty string")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(
                f"Validation failed for server '{server_name}': {str(e)}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        servers_path = app_context.settings['paths.servers'] if app_context and 'paths.servers' in app_context.settings else None
        if not servers_path or not os.path.exists(servers_path):
            raise AppFileNotFoundError(
                "Server base directory is not configured or does not exist")

        server_data = []
        errors = []

        for server_name in os.listdir(servers_path):
            server_dir = os.path.join(servers_path, server_name)
            if os.path.isdir(server_dir):
                try:
                    if self.validate_server(server_name, app_context):
                        server = BedrockServer(server_name, app_context)
                        status = server.get_status()
                        version = server.get_version()
                        server_data.append({
                            "name": server_name,
                            "status": status,
                            "version": version
                        })
                except Exception as e:
                    errors.append(
                        f"Error processing server '{server_name}': {str(e)}")

        server_data.sort(key=lambda x: x["name"])
        return server_data, errors
