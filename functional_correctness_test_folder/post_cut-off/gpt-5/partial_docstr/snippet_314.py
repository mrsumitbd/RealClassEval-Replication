from typing import Optional, Tuple, List, Dict, Any
import os
import logging


class DiscoveryMixin:
    def _get_logger(self, app_context: Optional["AppContext"]) -> logging.Logger:
        logger = getattr(app_context, "logger",
                         None) if app_context is not None else None
        return logger if isinstance(logger, logging.Logger) else logging.getLogger(__name__)

    def _import_errors(self):
        InvalidServerNameError = ConfigurationError = MissingArgumentError = AppFileNotFoundError = None
        # Try relative import style
        try:
            from .error import (  # type: ignore
                InvalidServerNameError as _InvalidServerNameError,
                ConfigurationError as _ConfigurationError,
                MissingArgumentError as _MissingArgumentError,
                AppFileNotFoundError as _AppFileNotFoundError,
            )
            InvalidServerNameError = _InvalidServerNameError
            ConfigurationError = _ConfigurationError
            MissingArgumentError = _MissingArgumentError
            AppFileNotFoundError = _AppFileNotFoundError
        except Exception:
            # Try absolute import fallback
            try:
                from error import (  # type: ignore
                    InvalidServerNameError as _InvalidServerNameError,
                    ConfigurationError as _ConfigurationError,
                    MissingArgumentError as _MissingArgumentError,
                    AppFileNotFoundError as _AppFileNotFoundError,
                )
                InvalidServerNameError = _InvalidServerNameError
                ConfigurationError = _ConfigurationError
                MissingArgumentError = _MissingArgumentError
                AppFileNotFoundError = _AppFileNotFoundError
            except Exception:
                pass
        return InvalidServerNameError, ConfigurationError, MissingArgumentError, AppFileNotFoundError

    def _instantiate_server(self, server_name: str, app_context: Optional["AppContext"]):
        server_cls = None
        # Try relative import style
        try:
            from .core.bedrock_server import BedrockServer as _BedrockServer  # type: ignore
            server_cls = _BedrockServer
        except Exception:
            # Try absolute import fallback
            try:
                from core.bedrock_server import BedrockServer as _BedrockServer  # type: ignore
                server_cls = _BedrockServer
            except Exception as e:
                raise e
        try:
            # type: ignore
            return server_cls(server_name, app_context=app_context)
        except TypeError:
            return server_cls(server_name)  # type: ignore

    def _get_servers_base_dir(self, app_context: Optional["AppContext"]) -> Optional[str]:
        settings = getattr(app_context, "settings",
                           None) if app_context is not None else None
        if not isinstance(settings, dict):
            return None
        # Direct key 'paths.servers'
        if "paths.servers" in settings and isinstance(settings.get("paths.servers"), str):
            return settings.get("paths.servers")
        # Nested dict paths -> servers
        paths = settings.get("paths")
        if isinstance(paths, dict):
            value = paths.get("servers")
            if isinstance(value, str):
                return value
        return None

    def validate_server(self, server_name: str, app_context: Optional["AppContext"] = None) -> bool:
        logger = self._get_logger(app_context)
        InvalidServerNameError, ConfigurationError, MissingArgumentError, _ = self._import_errors()

        if not server_name:
            if MissingArgumentError is not None:
                raise MissingArgumentError("server_name must not be empty")
            raise ValueError("server_name must not be empty")

        try:
            server = self._instantiate_server(server_name, app_context)
            is_installed = getattr(server, "is_installed", None)
            if callable(is_installed):
                return bool(is_installed())
            return False
        except Exception as e:
            expected = tuple(
                ex for ex in (InvalidServerNameError, ConfigurationError) if ex is not None
            )
            if expected and isinstance(e, expected):
                logger.warning(
                    "Validation failed for server '%s': %s", server_name, e)
            else:
                logger.warning(
                    "Validation error for server '%s': %s", server_name, e)
            return False

    def get_servers_data(self, app_context: Optional["AppContext"] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        logger = self._get_logger(app_context)
        _, _, _, AppFileNotFoundError = self._import_errors()

        base_dir = self._get_servers_base_dir(app_context)
        if not base_dir or not os.path.isdir(base_dir):
            msg = "Servers base directory is not configured or does not exist"
            if AppFileNotFoundError is not None:
                raise AppFileNotFoundError(msg)
            raise FileNotFoundError(msg)

        servers: List[Dict[str, Any]] = []
        errors: List[str] = []

        try:
            entries = sorted(os.listdir(base_dir))
        except Exception as e:
            msg = f"Failed to list servers directory '{base_dir}': {e}"
            if AppFileNotFoundError is not None:
                raise AppFileNotFoundError(msg)
            raise FileNotFoundError(msg)

        for name in entries:
            path = os.path.join(base_dir, name)
            if not os.path.isdir(path):
                continue
            try:
                server = self._instantiate_server(name, app_context)
                is_installed = getattr(server, "is_installed", None)
                if callable(is_installed) and not is_installed():
                    continue

                get_status = getattr(server, "get_status", None)
                get_version = getattr(server, "get_version", None)

                status = get_status() if callable(get_status) else "UNKNOWN"
                version = get_version() if callable(get_version) else "UNKNOWN"

                servers.append(
                    {
                        "name": name,
                        "status": status,
                        "version": version,
                    }
                )
            except Exception as e:
                logger.warning(
                    "Error processing server candidate '%s': %s", name, e)
                errors.append(f"{name}: {e}")

        servers.sort(key=lambda d: d.get("name", ""))

        return servers, errors
