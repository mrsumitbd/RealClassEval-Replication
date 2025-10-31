from typing import Optional, Tuple, List, Dict, Any

import logging
import os

# These imports assume the surrounding package layout as described in the docstrings.
# They will be resolved in the actual application environment.
try:
    from .core.bedrock_server import BedrockServer
    from .error import (
        InvalidServerNameError,
        ConfigurationError,
        MissingArgumentError,
        AppFileNotFoundError,
    )
except Exception:  # Fallbacks for static analysis or environments without package
    BedrockServer = object  # type: ignore

    class InvalidServerNameError(Exception):
        pass

    class ConfigurationError(Exception):
        pass

    class MissingArgumentError(Exception):
        pass

    class AppFileNotFoundError(FileNotFoundError):
        pass


class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
    '''

    def _get_app_context(self, app_context: Optional["AppContext"] = None) -> Optional["AppContext"]:
        if app_context is not None:
            return app_context
        return getattr(self, "app_context", None)

    def _get_logger(self, app_context: Optional["AppContext"]) -> logging.Logger:
        if app_context is not None and hasattr(app_context, "logger") and app_context.logger:
            return app_context.logger  # type: ignore[attr-defined]
        return logging.getLogger(__name__)

    def _get_settings(self, app_context: Optional["AppContext"]) -> Optional[dict]:
        if app_context is not None and hasattr(app_context, "settings"):
            return app_context.settings  # type: ignore[attr-defined]
        return getattr(self, "settings", None)

    def _get_servers_base_path(self, app_context: Optional["AppContext"]) -> str:
        settings = self._get_settings(app_context)
        try:
            servers_base = settings["paths"]["servers"]  # type: ignore[index]
        except Exception as e:
            raise AppFileNotFoundError(
                "Server base directory is not configured in settings['paths.servers']") from e
        if not servers_base or not isinstance(servers_base, str) or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                f"Server base directory not found: {servers_base!r}")
        return servers_base

    def validate_server(self, server_name: str, app_context: Optional["AppContext"] = None) -> bool:
        if not server_name:
            raise MissingArgumentError(
                "server_name must be a non-empty string")
        ctx = self._get_app_context(app_context)
        logger = self._get_logger(ctx)
        try:
            # type: ignore[call-arg]
            server = BedrockServer(server_name, app_context=ctx)
            return bool(getattr(server, "is_installed")())
        except (InvalidServerNameError, ConfigurationError) as exc:
            logger.warning(
                "Validation failed for server '%s': %s", server_name, exc)
            return False
        except Exception as exc:
            logger.warning(
                "Unexpected error validating server '%s': %s", server_name, exc)
            return False

    def get_servers_data(self, app_context: Optional["AppContext"] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        ctx = self._get_app_context(app_context)
        logger = self._get_logger(ctx)
        base_path = self._get_servers_base_path(ctx)

        servers: List[Dict[str, Any]] = []
        errors: List[str] = []

        try:
            entries = os.listdir(base_path)
        except Exception as e:
            raise AppFileNotFoundError(
                f"Unable to list server base directory: {base_path!r}") from e

        for name in sorted(entries):
            full_path = os.path.join(base_path, name)
            if not os.path.isdir(full_path):
                continue
            try:
                # type: ignore[call-arg]
                server = BedrockServer(name, app_context=ctx)
                if not getattr(server, "is_installed")():
                    continue
                status = getattr(server, "get_status")()
                version = getattr(server, "get_version")()
                servers.append(
                    {
                        "name": name,
                        "status": status,
                        "version": version,
                    }
                )
            except (InvalidServerNameError, ConfigurationError) as exc:
                msg = f"Error processing server '{name}': {exc}"
                errors.append(msg)
                logger.warning(msg)
            except Exception as exc:
                msg = f"Unexpected error processing server '{name}': {exc}"
                errors.append(msg)
                logger.warning(msg)

        servers.sort(key=lambda x: x.get("name", ""))
        return servers, errors
