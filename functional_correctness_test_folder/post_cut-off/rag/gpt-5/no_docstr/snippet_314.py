from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from .core.bedrock_server import BedrockServer
from .error import (
    AppFileNotFoundError,
    ConfigurationError,
    InvalidServerNameError,
    MissingArgumentError,
)

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
        if server_name is None or not str(server_name).strip():
            raise MissingArgumentError(
                "Parameter 'server_name' must be a non-empty string.")

        try:
            try:
                server = BedrockServer(server_name, app_context=app_context)
            except TypeError:
                # Fallbacks for potential constructor variations.
                if app_context is not None:
                    try:
                        server = BedrockServer(server_name, app_context)
                    except TypeError:
                        server = BedrockServer(server_name)
                else:
                    server = BedrockServer(server_name)
            return bool(server.is_installed())
        except (InvalidServerNameError, ConfigurationError) as e:
            logger.warning(
                "Validation failed for server '%s': %s", server_name, e)
            return False
        except Exception as e:
            logger.warning(
                "Unexpected error validating server '%s': %s", server_name, e)
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
        base_dir = self._resolve_servers_base_dir(app_context)

        if not base_dir or not isinstance(base_dir, str):
            raise AppFileNotFoundError(
                "Settings 'paths.servers' is not configured.")
        if not os.path.isdir(base_dir):
            raise AppFileNotFoundError(
                f"Servers base directory not found: {base_dir}")

        servers_data: List[Dict[str, Any]] = []
        errors: List[str] = []

        try:
            entries = list(os.scandir(base_dir))
        except OSError as e:
            raise AppFileNotFoundError(
                f"Unable to read servers base directory '{base_dir}': {e}") from e

        for entry in entries:
            if not entry.is_dir(follow_symlinks=False):
                continue

            server_name = entry.name
            try:
                try:
                    server = BedrockServer(
                        server_name, app_context=app_context)
                except TypeError:
                    if app_context is not None:
                        try:
                            server = BedrockServer(server_name, app_context)
                        except TypeError:
                            server = BedrockServer(server_name)
                    else:
                        server = BedrockServer(server_name)

                if not server.is_installed():
                    continue

                status = server.get_status()
                version = server.get_version()

                servers_data.append(
                    {
                        "name": server_name,
                        "status": status,
                        "version": version,
                    }
                )
            except (InvalidServerNameError, ConfigurationError) as e:
                msg = f"Error processing server '{server_name}': {e}"
                logger.warning(msg)
                errors.append(msg)
            except Exception as e:
                msg = f"Unexpected error processing server '{server_name}': {e}"
                logger.warning(msg)
                errors.append(msg)

        servers_data.sort(key=lambda x: x.get("name", ""))

        return servers_data, errors

    def _resolve_servers_base_dir(self, app_context: Optional['AppContext']) -> Optional[str]:
        # Attempt to retrieve settings from app_context first, then self.
        settings_sources: List[Any] = []
        if app_context is not None:
            if hasattr(app_context, "settings"):
                settings_sources.append(getattr(app_context, "settings"))
            if hasattr(app_context, "get_settings"):
                try:
                    settings_sources.append(app_context.get_settings())
                except Exception:
                    pass
        if hasattr(self, "settings"):
            settings_sources.append(getattr(self, "settings"))
        if hasattr(self, "get_settings"):
            try:
                settings_sources.append(self.get_settings())
            except Exception:
                pass

        for s in settings_sources:
            # Try dotted access via get
            val = None
            try:
                if hasattr(s, "get"):
                    val = s.get("paths.servers")
            except Exception:
                val = None

            if not val:
                # Try nested dict-like access
                val = self._get_nested(s, "paths", "servers")

            if val:
                return str(val)

        return None

    @staticmethod
    def _get_nested(container: Any, *keys: str) -> Optional[Any]:
        cur = container
        for k in keys:
            if cur is None:
                return None
            if isinstance(cur, dict):
                if k in cur:
                    cur = cur[k]
                else:
                    try:
                        cur = cur.get(k)  # type: ignore[attr-defined]
                    except Exception:
                        return None
            else:
                if hasattr(cur, "get"):
                    try:
                        cur = cur.get(k)  # type: ignore[attr-defined]
                    except Exception:
                        return None
                elif hasattr(cur, k):
                    cur = getattr(cur, k)
                else:
                    return None
        return cur
