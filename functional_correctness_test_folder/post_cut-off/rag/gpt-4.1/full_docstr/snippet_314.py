import os
import logging
from typing import Optional, List, Dict, Any, Tuple

from .core.bedrock_server import BedrockServer
from .error import InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError

logger = logging.getLogger(__name__)


class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
    '''

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        '''Validates if a given server name corresponds to a valid installation.
        This method checks for the existence and basic integrity of a server
        installation. It instantiates a :class:`~.core.bedrock_server.BedrockServer`
        object for the given ``server_name`` and then calls its
        :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
        Any exceptions raised during the instantiation or validation process (e.g.,
        :class:`~.error.InvalidServerNameError`, :class:`~.error.ConfigurationError`)
        are caught, logged as a warning, and result in a ``False`` return value,
        making this a safe check.
        Args:
            server_name (str): The name of the server to validate. This should
                correspond to a subdirectory within the main server base directory.
        Returns:
            bool: ``True`` if the server exists and is a valid installation
            (i.e., its directory and executable are found), ``False`` otherwise.
        Raises:
            MissingArgumentError: If ``server_name`` is an empty string.
        '''
        if not server_name or not server_name.strip():
            raise MissingArgumentError("server_name must not be empty")
        try:
            server = BedrockServer(server_name, app_context=app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logger.warning(
                f"Validation failed for server '{server_name}': {e}")
            return False
        except Exception as e:
            logger.warning(
                f"Unexpected error during validation of server '{server_name}': {e}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        '''Discovers and retrieves status data for all valid server instances.
        This method scans the main server base directory (defined by
        ``settings['paths.servers']``) for subdirectories that represent server
        installations. For each potential server, it:
            1. Instantiates a :class:`~.core.bedrock_server.BedrockServer` object.
            2. Validates the installation using the server's :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
            3. If valid, it queries the server's status and version using
               :meth:`~.core.bedrock_server.BedrockServer.get_status` and
               :meth:`~.core.bedrock_server.BedrockServer.get_version`.
        Errors encountered while processing individual servers are collected and
        returned separately, allowing the method to succeed even if some server
        directories are corrupted or misconfigured. The final list of server
        data is sorted alphabetically by server name.
        Returns:
            Tuple[List[Dict[str, Any]], List[str]]: A tuple containing two lists:
                - The first list contains dictionaries, one for each successfully
                  processed server. Each dictionary has the keys:
                    - ``"name"`` (str): The name of the server.
                    - ``"status"`` (str): The server's current status (e.g., "RUNNING", "STOPPED").
                    - ``"version"`` (str): The detected version of the server.
                - The second list contains string messages describing any errors that
                  occurred while processing specific server candidates.
        Raises:
            AppFileNotFoundError: If the main server base directory
                (``settings['paths.servers']``) is not configured or does not exist.
        '''
        # Assume self.settings is available, or app_context.settings
        settings = getattr(self, 'settings', None)
        if settings is None and app_context is not None:
            settings = getattr(app_context, 'settings', None)
        if settings is None:
            raise AppFileNotFoundError(
                "Settings not found for server discovery.")

        servers_base = settings.get('paths.servers')
        if not servers_base or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                f"Server base directory '{servers_base}' does not exist or is not configured.")

        server_data: List[Dict[str, Any]] = []
        errors: List[str] = []

        try:
            candidates = [
                name for name in os.listdir(servers_base)
                if os.path.isdir(os.path.join(servers_base, name))
            ]
        except Exception as e:
            raise AppFileNotFoundError(
                f"Failed to list server base directory '{servers_base}': {e}")

        for server_name in candidates:
            try:
                server = BedrockServer(server_name, app_context=app_context)
                if not server.is_installed():
                    continue
                status = server.get_status()
                version = server.get_version()
                server_data.append({
                    "name": server_name,
                    "status": status,
                    "version": version
                })
            except (InvalidServerNameError, ConfigurationError) as e:
                msg = f"Server '{server_name}': {e}"
                logger.warning(msg)
                errors.append(msg)
            except Exception as e:
                msg = f"Server '{server_name}': Unexpected error: {e}"
                logger.warning(msg)
                errors.append(msg)

        server_data.sort(key=lambda d: d["name"])
        return server_data, errors
