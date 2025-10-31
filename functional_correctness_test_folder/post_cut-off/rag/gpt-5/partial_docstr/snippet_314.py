import os
import logging
from typing import Optional, Tuple, List, Dict, Any

try:
    from .core.bedrock_server import BedrockServer
except Exception:
    try:
        from core.bedrock_server import BedrockServer  # type: ignore
    except Exception:  # pragma: no cover - fallback for environments without package context
        BedrockServer = None  # type: ignore

try:
    from .error import (
        InvalidServerNameError,
        ConfigurationError,
        MissingArgumentError,
        AppFileNotFoundError,
    )
except Exception:
    try:
        from error import (  # type: ignore
            InvalidServerNameError,
            ConfigurationError,
            MissingArgumentError,
            AppFileNotFoundError,
        )
    except Exception:  # pragma: no cover - fallback for environments without package context
        class MissingArgumentError(ValueError):
            pass

        class InvalidServerNameError(Exception):
            pass

        class ConfigurationError(Exception):
            pass

        class AppFileNotFoundError(FileNotFoundError):
            pass

try:
    from .app_context import AppContext  # type: ignore
except Exception:
    try:
        from .core.app_context import AppContext  # type: ignore
    except Exception:  # type: ignore
        AppContext = Any  # type: ignore


class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
        '''

    def _create_bedrock_server(self, server_name: str, app_context: Optional[AppContext]):
        # Try common constructor signatures to maximize compatibility.
        # Prefer keyword to avoid positional ambiguity.
        try:
            # type: ignore[arg-type]
            return BedrockServer(server_name, app_context=app_context)
        except TypeError:
            pass
        try:
            # type: ignore[misc]
            return BedrockServer(server_name, app_context)
        except TypeError:
            pass
        try:
            # type: ignore[misc]
            return BedrockServer(app_context, server_name)
        except TypeError:
            # Fall back to name-only if context not required.
            return BedrockServer(server_name)  # type: ignore[misc]

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
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
        if not server_name or not str(server_name).strip():
            raise MissingArgumentError("server_name must not be empty")

        ctx = app_context if app_context is not None else getattr(
            self, "app_context", None)
        try:
            server = self._create_bedrock_server(server_name, ctx)
            return bool(server.is_installed())
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(
                "Validation failed for server '%s': %s", server_name, e)
            return False
        except Exception as e:
            logging.warning(
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
        ctx = app_context if app_context is not None else getattr(
            self, "app_context", None)
        settings = None

        # Resolve settings from context or self
        if ctx is not None and hasattr(ctx, "settings"):
            settings = getattr(ctx, "settings")
        elif hasattr(self, "settings"):
            settings = getattr(self, "settings")

        base_dir = None
        if settings is not None:
            try:
                if hasattr(settings, "get"):
                    # type: ignore[attr-defined]
                    base_dir = settings.get("paths.servers", None)
            except Exception:
                base_dir = None

            if not base_dir and isinstance(settings, dict):
                paths = settings.get("paths")
                if isinstance(paths, dict):
                    base_dir = paths.get("servers")

        if not base_dir or not isinstance(base_dir, str):
            raise AppFileNotFoundError(
                "settings['paths.servers'] is not configured")

        if not os.path.isdir(base_dir):
            raise AppFileNotFoundError(
                f"Server base directory not found: {base_dir}")

        try:
            entries = os.listdir(base_dir)
        except Exception as e:
            raise AppFileNotFoundError(
                f"Unable to list server base directory '{base_dir}': {e}") from e

        servers_data: List[Dict[str, Any]] = []
        errors: List[str] = []

        for name in entries:
            server_path = os.path.join(base_dir, name)
            if not os.path.isdir(server_path):
                continue

            try:
                server = self._create_bedrock_server(name, ctx)
                if not server.is_installed():
                    continue

                status = server.get_status()
                version = server.get_version()
                servers_data.append(
                    {
                        "name": name,
                        "status": status,
                        "version": version,
                    }
                )
            except (InvalidServerNameError, ConfigurationError) as e:
                msg = f"{name}: {e}"
                logging.warning("Error processing server '%s': %s", name, e)
                errors.append(msg)
            except Exception as e:
                msg = f"{name}: {e}"
                logging.warning(
                    "Unexpected error processing server '%s': %s", name, e)
                errors.append(msg)

        servers_data.sort(key=lambda x: x.get("name", "").lower())
        return servers_data, errors
