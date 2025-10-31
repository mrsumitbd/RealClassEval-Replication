
import os
import logging
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError


class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
    '''

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        '''Validates if a given server name corresponds to a valid installation.'''
        if not server_name:
            raise MissingArgumentError("server_name cannot be an empty string")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(f"Error validating server {server_name}: {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        '''Discovers and retrieves status data for all valid server instances.'''
        servers_base_dir = app_context.settings.get('paths.servers')
        if not servers_base_dir or not os.path.isdir(servers_base_dir):
            raise AppFileNotFoundError(
                f"Server base directory not found: {servers_base_dir}")

        servers_data = []
        errors = []

        for server_dir in os.listdir(servers_base_dir):
            server_path = Path(servers_base_dir) / server_dir
            if not server_path.is_dir():
                continue

            try:
                server = BedrockServer(server_dir, app_context)
                if server.is_installed():
                    status = server.get_status()
                    version = server.get_version()
                    servers_data.append({
                        "name": server_dir,
                        "status": status,
                        "version": version
                    })
            except Exception as e:
                errors.append(f"Error processing server {server_dir}: {e}")

        servers_data.sort(key=lambda x: x["name"])
        return servers_data, errors
