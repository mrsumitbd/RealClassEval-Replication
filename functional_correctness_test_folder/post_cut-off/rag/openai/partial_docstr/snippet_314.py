
import os
import logging
from typing import Any, Dict, List, Optional, Tuple

# Import the required classes and exceptions.  The exact import paths may vary
# depending on the project layout, but the names are taken from the docstring.
try:
    from .core.bedrock_server import BedrockServer
    from .error import (
        MissingArgumentError,
        AppFileNotFoundError,
        InvalidServerNameError,
        ConfigurationError,
    )
except Exception:  # pragma: no cover
    # In case the relative imports fail (e.g., when the module is imported
    # from a different package structure), fall back to absolute imports.
    from core.bedrock_server import BedrockServer
    from error import (
        MissingArgumentError,
        AppFileNotFoundError,
        InvalidServerNameError,
        ConfigurationError,
    )

log = logging.getLogger(__name__)


class DiscoveryMixin:
    """
    Mixin class for BedrockServerManager that handles server discovery and validation.
    """

    def validate_server(
        self, server_name: str, app_context: Optional["AppContext"] = None
    ) -> bool:
        """
        Validates if a given server name corresponds to a valid installation.
        This method checks for the existence and basic integrity of a server
        installation. It instantiates a :class:`~.core.bedrock_server.BedrockServer`
        object for the given ``server_name`` and then calls its
        :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
        Any exceptions raised during the instantiation or validation process
        (e.g., :class:`~.error.InvalidServerNameError`,
        :class:`~.error.ConfigurationError`) are caught, logged as a warning,
        and result in a ``False`` return value, making this a safe check.
        Args:
            server_name (str): The name of the server to validate. This should
                correspond to a subdirectory within the main server base directory.
        Returns:
            bool: ``True`` if the server exists and is a valid installation
            (i.e., its directory and executable are found), ``False`` otherwise.
        Raises:
            MissingArgumentError: If ``server_name`` is an empty string.
        """
        if not server_name:
            raise MissingArgumentError("server_name must not be empty")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as exc:
            log.warning(
                "Server validation failed for '%s': %s", server_name, exc, exc_info=True
            )
            return False
        except Exception as exc:  # pragma: no cover
            log.warning(
                "Unexpected error during validation of server '%s': %s",
                server_name,
                exc,
                exc_info=True,
            )
            return False

    def get_servers_data(
        self, app_context: Optional["AppContext"] = None
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Discovers and retrieves status data for all valid server instances.
        This method scans the main server base directory (defined by
        ``settings['paths.servers']``) for subdirectories that represent server
        installations. For each potential server, it:
            1. Instantiates a :class:`~.core.bedrock_server.BedrockServer` object.
            2. Validates the installation using the server's
               :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
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
        """
        # Resolve the base directory from the application context or settings.
        if app_context is None:
            # If no context is provided, attempt to import a global one.
            try:
                from .app_context import AppContext

                app_context = AppContext.get_default()
            except Exception:  # pragma: no cover
                app_context = None

        # Retrieve the servers path from settings.
        try:
            servers_path = app_context.settings["paths"]["servers"]
        except Exception as exc:  # pragma: no cover
            raise AppFileNotFoundError(
                "Missing or invalid 'paths.servers' configuration"
            ) from exc

        if not os.path.isdir(servers_path):
            raise AppFileNotFoundError(
                f"Server base directory not found: {servers_path}"
            )

        server_data: List[Dict[str, Any]] = []
        error_messages: List[str] = []

        for entry in os.listdir(servers_path):
            full_path = os.path.join(servers_path, entry)
            if not os.path.isdir(full_path):
                continue  # Skip non-directory entries

            try:
                server = BedrockServer(entry, app_context)
                if not server.is_installed():
                    continue  # Skip invalid installations

                status = server.get_status()
                version = server.get_version()
                server_data.append(
                    {"name": entry, "status": status, "version": version}
                )
            except (InvalidServerNameError, ConfigurationError) as exc:
                error_messages.append(
                    f"Server '{entry}': configuration error: {exc}"
                )
            except Exception as exc:  # pragma: no cover
                error_messages.append(
                    f"Server '{entry}': unexpected error: {exc}"
                )

        # Sort the data alphabetically by server name.
        server_data.sort(key=lambda d: d["name"])
        return server_data, error_messages
