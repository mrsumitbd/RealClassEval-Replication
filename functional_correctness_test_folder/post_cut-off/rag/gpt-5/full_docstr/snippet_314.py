import logging
import os
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .app_context import AppContext

from .error import (
    AppFileNotFoundError,
    ConfigurationError,
    InvalidServerNameError,
    MissingArgumentError,
)


class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
    '''

    def validate_server(self, server_name: str, app_context: Optional["AppContext"] = None) -> bool:
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
        logger = logging.getLogger(__name__)

        if server_name is None or not str(server_name).strip():
            raise MissingArgumentError(
                "validate_server: 'server_name' must be a non-empty string.")

        # Resolve app context if not provided
        ctx = app_context if app_context is not None else getattr(
            self, "app_context", None)

        try:
            from .core.bedrock_server import BedrockServer

            server = BedrockServer(server_name, app_context=ctx)
            return bool(server.is_installed())
        except (InvalidServerNameError, ConfigurationError) as exc:
            logger.warning(
                "Server validation failed for '%s': %s", server_name, exc)
            return False
        except Exception as exc:  # Safe check: any unexpected error means invalid
            logger.warning(
                "Unexpected error while validating server '%s': %s", server_name, exc)
            return False

    def get_servers_data(self, app_context: Optional["AppContext"] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
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
        logger = logging.getLogger(__name__)

        def _lookup_settings_path(settings_obj: Any, key_path: str) -> Optional[str]:
            # Try nested dict lookup
            if isinstance(settings_obj, dict):
                if key_path in settings_obj:
                    return settings_obj.get(key_path)
                value: Any = settings_obj
                for part in key_path.split("."):
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        return None
                return value if isinstance(value, str) else None

            # Try a dict-like get method that may accept key_path
            getter = getattr(settings_obj, "get", None)
            if callable(getter):
                try:
                    val = getter(key_path)
                    if isinstance(val, str):
                        return val
                except TypeError:
                    try:
                        val = getter(key_path, None)
                        if isinstance(val, str):
                            return val
                    except Exception:
                        pass

            # Try attribute traversal (dot path)
            value = settings_obj
            for part in key_path.split("."):
                if hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return None
            return value if isinstance(value, str) else None

        # Resolve app context and settings
        ctx = app_context if app_context is not None else getattr(
            self, "app_context", None)
        settings_obj = getattr(ctx, "settings", None) if ctx is not None else getattr(
            self, "settings", None)

        servers_base = _lookup_settings_path(
            settings_obj, "paths.servers") if settings_obj is not None else None
        if not servers_base or not isinstance(servers_base, str):
            raise AppFileNotFoundError(
                "Server base directory is not configured (settings['paths.servers']).")

        servers_base = os.path.expanduser(os.path.expandvars(servers_base))
        if not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                f"Server base directory does not exist: {servers_base}")

        try:
            entries = [e for e in os.scandir(servers_base) if e.is_dir()]
        except OSError as exc:
            raise AppFileNotFoundError(
                f"Unable to access server base directory '{servers_base}': {exc}") from exc

        # Sort candidate server names to ensure deterministic order
        candidate_names = sorted(e.name for e in entries)

        from .core.bedrock_server import BedrockServer

        servers: List[Dict[str, Any]] = []
        errors: List[str] = []

        for name in candidate_names:
            try:
                server = BedrockServer(name, app_context=ctx)

                try:
                    if not server.is_installed():
                        continue
                except Exception as exc:
                    msg = f"Error checking installation for server '{name}': {exc}"
                    logger.warning(msg)
                    errors.append(msg)
                    continue

                try:
                    status = server.get_status()
                except Exception as exc:
                    msg = f"Error retrieving status for server '{name}': {exc}"
                    logger.warning(msg)
                    errors.append(msg)
                    continue

                try:
                    version = server.get_version()
                except Exception as exc:
                    msg = f"Error retrieving version for server '{name}': {exc}"
                    logger.warning(msg)
                    errors.append(msg)
                    continue

                servers.append(
                    {
                        "name": name,
                        "status": status,
                        "version": version,
                    }
                )

            except (InvalidServerNameError, ConfigurationError) as exc:
                msg = f"Configuration error for server '{name}': {exc}"
                logger.warning(msg)
                errors.append(msg)
            except Exception as exc:
                msg = f"Unexpected error processing server '{name}': {exc}"
                logger.warning(msg)
                errors.append(msg)

        # Ensure servers are sorted by name
        servers.sort(key=lambda s: s.get("name", ""))

        return servers, errors
