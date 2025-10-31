
import os
import logging
from typing import Optional, List, Dict, Any, Tuple

# Assume these are imported from the correct modules
# from .core.bedrock_server import BedrockServer
# from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError

# For the sake of completeness, let's define minimal placeholder exceptions and classes.


class InvalidServerNameError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class MissingArgumentError(Exception):
    pass


class AppFileNotFoundError(Exception):
    pass


class BedrockServer:
    def __init__(self, name: str, app_context: Optional['AppContext'] = None):
        if not name or '/' in name or '\\' in name:
            raise InvalidServerNameError("Invalid server name")
        self.name = name
        self.app_context = app_context
        # Simulate a path for the server
        self.base_path = (
            app_context.settings['paths.servers'] if app_context else settings['paths.servers'])
        self.path = os.path.join(self.base_path, name)
        if not os.path.isdir(self.path):
            raise ConfigurationError("Server directory does not exist")

    def is_installed(self) -> bool:
        # Simulate: installed if directory exists and "bedrock_server" file exists
        exe_path = os.path.join(self.path, "bedrock_server")
        return os.path.isdir(self.path) and os.path.isfile(exe_path)

    def get_status(self) -> str:
        # Simulate status
        return "RUNNING" if os.path.exists(os.path.join(self.path, "running")) else "STOPPED"

    def get_version(self) -> str:
        # Simulate version
        version_file = os.path.join(self.path, "version.txt")
        if os.path.isfile(version_file):
            with open(version_file, "r") as f:
                return f.read().strip()
        return "unknown"


# Simulate a settings object
settings = {
    'paths.servers': '/tmp/bedrock_servers'
}


class AppContext:
    def __init__(self, settings_dict=None):
        self.settings = settings_dict if settings_dict else settings


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        if not server_name:
            raise MissingArgumentError("server_name is required")
        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(
                f"Validation failed for server '{server_name}': {e}")
            return False
        except Exception as e:
            logging.warning(
                f"Unexpected error during validation of server '{server_name}': {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        ctx = app_context if app_context else AppContext()
        servers_base = ctx.settings.get('paths.servers')
        if not servers_base or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                f"Server base directory '{servers_base}' not found or not configured")
        server_data = []
        errors = []
        try:
            candidates = [
                name for name in os.listdir(servers_base)
                if os.path.isdir(os.path.join(servers_base, name))
            ]
        except Exception as e:
            raise AppFileNotFoundError(
                f"Failed to list server base directory: {e}")
        for name in candidates:
            try:
                server = BedrockServer(name, ctx)
                if not server.is_installed():
                    continue
                status = server.get_status()
                version = server.get_version()
                server_data.append({
                    "name": name,
                    "status": status,
                    "version": version
                })
            except (InvalidServerNameError, ConfigurationError) as e:
                errors.append(f"Server '{name}': {e}")
            except Exception as e:
                errors.append(f"Server '{name}': Unexpected error: {e}")
        server_data.sort(key=lambda x: x["name"])
        return server_data, errors
