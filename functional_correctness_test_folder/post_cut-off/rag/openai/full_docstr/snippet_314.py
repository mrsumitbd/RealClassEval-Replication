
import os
import logging
from typing import Any, Dict, List, Optional, Tuple

# Import the required classes and exceptions.  The exact import paths may
# differ in the real project; adjust as necessary.
try:
    from .core.bedrock_server import BedrockServer
    from .error import (
        MissingArgumentError,
        AppFileNotFoundError,
        InvalidServerNameError,
        ConfigurationError,
    )
except Exception:  # pragma: no cover
    # In case the imports fail during static analysis, provide stubs so the
    # module can still be imported.  The real implementation will replace
    # these with the actual classes.
    class BedrockServer:  # type: ignore
        def __init__(self, name: str, app_context: Optional[Any] = None):
            self.name = name

        def is_installed(self) -> bool:
            return True

        def get_status(self) -> str:
            return "RUNNING"

        def get_version(self) -> str:
            return "1.0.0"

    class MissingArgumentError(Exception):
        pass

    class AppFileNotFoundError(Exception):
        pass

    class InvalidServerNameError(Exception):
        pass

    class ConfigurationError(Exception):
        pass


class DiscoveryMixin:
    """
    Mixin class for BedrockServerManager that handles server discovery and validation.
    """

    _log = logging.getLogger(__name__)

    def _get_settings(self, app_context: Optional[Any]) -> Dict[str, Any]:
        """
        Helper to obtain the settings dictionary from the application context.
        """
        if app_context is None:
            # If no context is provided, attempt to use a global context.
            # This is a placeholder; replace with the actual global context
            # retrieval logic if available.
            if hasattr(self, "app_context"):
                app_context = self.app_context
            else:
                raise AppFileNotFoundError("No application context available.")
        return getattr(app_context, "settings", {})

    def validate_server(
        self, server_name: str, app_context: Optional[Any] = None
    ) -> bool:
        """
        Validates if a given server name corresponds to a valid installation.
        """
        if not server_name:
            raise MissingArgumentError("server_name must not be empty")

        try:
            settings = self._get_settings(app_context)
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as exc:
            self._log.warning(
                "Validation failed for server '%s': %s", server_name, exc
            )
            return False
        except Exception as exc:  # pragma: no cover
            self._log.warning(
                "Unexpected error validating server '%s': %s", server_name, exc
            )
            return False

    def get_servers_data(
        self, app_context: Optional[Any] = None
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Discovers and retrieves status data for all valid server instances.
        """
        settings = self._get_settings(app_context)
        servers_path = settings.get("paths", {}).get("servers")

        if not servers_path:
            raise AppFileNotFoundError(
                "The 'paths.servers' setting is not configured."
            )

        if not os.path.isdir(servers_path):
            raise AppFileNotFoundError(
                f"Server base directory '{servers_path}' does not exist."
            )

        server_data: List[Dict[str, Any]] = []
        error_messages: List[str] = []

        for entry in os.listdir(servers_path):
            full_path = os.path.join(servers_path, entry)
            if not os.path.isdir(full_path):
                continue  # Skip non‑directory entries

            try:
                server = BedrockServer(entry, app_context)
                if not server.is_installed():
                    continue

                status = server.get_status()
                version = server.get_version()
                server_data.append(
                    {"name": entry, "status": status, "version": version}
                )
            except Exception as exc:  # pragma: no cover
                msg = f"Error processing server '{entry}': {exc}"
                self._log.warning(msg)
                error_messages.append(msg)

        # Sort the data alphabetically by server name
        server_data.sort(key=lambda d: d["name"])
        return server_data, error_messages
