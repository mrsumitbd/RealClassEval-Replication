from typing import Dict, Optional
import os
import platform
import shutil
import logging

try:
    from importlib.metadata import version as pkg_version, PackageNotFoundError  # Python 3.8+
except Exception:  # pragma: no cover
    try:
        from importlib_metadata import version as pkg_version, PackageNotFoundError  # type: ignore
    except Exception:  # pragma: no cover
        pkg_version = None  # type: ignore
        PackageNotFoundError = Exception  # type: ignore

try:  # Windows admin check
    import ctypes
except Exception:  # pragma: no cover
    ctypes = None  # type: ignore


class SystemMixin:
    _capabilities: Optional[Dict[str, bool]] = None

    def get_app_version(self) -> str:
        if hasattr(self, "__version__") and isinstance(getattr(self, "__version__"), str):
            return getattr(self, "__version__")  # type: ignore
        if hasattr(self, "version") and isinstance(getattr(self, "version"), str):
            return getattr(self, "version")  # type: ignore

        env_ver = os.getenv("APP_VERSION")
        if env_ver:
            return env_ver

        root_module = ""
        try:
            root_module = self.__class__.__module__.split(".")[0]
        except Exception:
            pass

        if pkg_version and root_module:
            try:
                return pkg_version(root_module)  # type: ignore
            except PackageNotFoundError:
                pass
            except Exception:
                pass

        return "0.0.0"

    def get_os_type(self) -> str:
        sys = platform.system().lower()
        if "windows" in sys:
            return "windows"
        if "darwin" in sys or "mac" in sys:
            return "darwin"
        if "linux" in sys:
            return "linux"
        return sys or "unknown"

    def _is_admin(self) -> bool:
        os_type = self.get_os_type()
        try:
            if os_type in ("linux", "darwin"):
                return os.geteuid() == 0  # type: ignore[attr-defined]
            if os_type == "windows":
                if ctypes and hasattr(ctypes, "windll"):
                    try:
                        # type: ignore[attr-defined]
                        return bool(ctypes.windll.shell32.IsUserAnAdmin())
                    except Exception:
                        return False
                return False
        except Exception:
            return False
        return False

    def _check_system_capabilities(self) -> Dict[str, bool]:
        if self._capabilities is not None:
            return self._capabilities

        os_type = self.get_os_type()
        is_admin = self._is_admin()

        # Scheduling tools presence
        has_crontab = shutil.which("crontab") is not None
        has_systemd_run = shutil.which("systemd-run") is not None
        has_launchctl = shutil.which("launchctl") is not None
        has_schtasks = shutil.which("schtasks") is not None or shutil.which(
            "schtasks.exe") is not None

        # Service management tools presence
        has_systemctl = shutil.which("systemctl") is not None
        has_service_cmd = shutil.which("service") is not None
        has_sc = shutil.which("sc") is not None or shutil.which(
            "sc.exe") is not None

        if os_type == "windows":
            can_schedule = bool(has_schtasks)
            can_manage = bool(has_sc and is_admin)
        elif os_type == "linux":
            can_schedule = bool(has_crontab or has_systemd_run)
            can_manage = bool(is_admin and (has_systemctl or has_service_cmd))
        elif os_type == "darwin":
            can_schedule = bool(has_launchctl)
            can_manage = bool(is_admin and has_launchctl)
        else:
            can_schedule = False
            can_manage = False

        self._capabilities = {
            "schedule_tasks": can_schedule,
            "manage_services": can_manage,
        }
        return self._capabilities

    def _log_capability_warnings(self) -> None:
        caps = self._check_system_capabilities()
        logger = logging.getLogger(__name__)

        if not caps.get("schedule_tasks", False):
            logger.warning(
                "Task scheduling capability is not available on this system. "
                "Ensure required tools are installed and accessible."
            )
        if not caps.get("manage_services", False):
            logger.warning(
                "Service management capability is not available or lacks sufficient privileges. "
                "Run with administrative privileges and ensure service management tools are installed."
            )

    @property
    def can_schedule_tasks(self) -> bool:
        return self._check_system_capabilities().get("schedule_tasks", False)

    @property
    def can_manage_services(self) -> bool:
        return self._check_system_capabilities().get("manage_services", False)
