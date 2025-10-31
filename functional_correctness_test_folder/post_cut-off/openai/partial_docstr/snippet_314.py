
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .core.bedrock_server import BedrockServer
from .error import (
    AppFileNotFoundError,
    ConfigurationError,
    InvalidServerNameError,
    MissingArgumentError,
)
from .settings import settings
from .app_context import AppContext

log = logging.getLogger(__name__)


class DiscoveryMixin:
    def validate_server(
        self, server_name: str, app_context: Optional[AppContext] = None
    ) -> bool:
        """
        Validates if a given server name corresponds to a valid installation.
        """
        if not server_name:
            raise MissingArgumentError("server_name must not be empty")

        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as exc:
            log.warning(
                "Failed to validate server '%s': %s", server_name, exc, exc_info=True
            )
            return False
        except Exception as exc:  # pragma: no cover
            log.warning(
                "Unexpected error while validating server '%s': %s",
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
        """
        servers_path = settings.get("paths", {}).get("servers")
        if not servers_path:
            raise AppFileNotFoundError(
                "Server base directory not configured in settings['paths.servers']"
            )

        base_dir = Path(servers_path)
        if not base_dir.is_dir():
            raise AppFileNotFoundError(
                f"Server base directory '{base_dir}' does not exist or is not a directory"
            )

        server_data: List[Dict[str, Any]] = []
        errors: List[str] = []

        for entry in sorted(base_dir.iterdir(), key=lambda p: p.name.lower()):
            if not entry.is_dir():
                continue

            server_name = entry.name
            try:
                server = BedrockServer(server_name, app_context)
                if not server.is_installed():
                    continue

                status = server.get_status()
                version = server.get_version()
                server_data.append(
                    {"name": server_name, "status": status, "version": version}
                )
            except (InvalidServerNameError, ConfigurationError) as exc:
                errors.append(
                    f"Server '{server_name}': {exc.__class__.__name__}: {exc}"
                )
            except Exception as exc:  # pragma: no cover
                errors.append(
                    f"Server '{server_name}': Unexpected error: {exc}"
                )

        # Sort the data alphabetically by server name
        server_data.sort(key=lambda d: d["name"].lower())

        return server_data, errors
