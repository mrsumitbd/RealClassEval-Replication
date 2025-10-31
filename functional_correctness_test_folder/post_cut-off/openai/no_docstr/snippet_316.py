
import logging
import platform
from typing import Dict

try:
    # Python 3.8+
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Backport for older Python
    from importlib_metadata import version, PackageNotFoundError

log = logging.getLogger(__name__)


class SystemMixin:
    """
    Mixin providing basic system information and capability checks.
    """

    def get_app_version(self) -> str:
        """
        Return the application version string.

        Attempts to read the version from package metadata. If the package
        cannot be found, falls back to a default placeholder.
        """
        # Try to infer the package name from the module's __package__ attribute.
        pkg_name = self.__class__.__module__.split('.')[0]
        try:
            return version(pkg_name)
        except PackageNotFoundError:
            # Fallback: use a generic placeholder
            return "0.0.0"

    def get_os_type(self) -> str:
        """
        Return the operating system type as a string.
        """
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        """
        Detect system capabilities for scheduling tasks and managing services.

        Returns a dictionary with keys:
            - 'can_schedule_tasks'
            - 'can_manage_services'
        """
        os_type = self.get_os_type()
        # Default to False for unknown OS
        can_schedule = False
        can_manage = False

        if os_type == "Windows":
            # Windows Task Scheduler and Service Control Manager
            can_schedule = True
            can_manage = True
        elif os_type == "Linux":
            # Assume cron and systemd are available
            can_schedule = True
            can_manage = True
        elif os_type == "Darwin":
            # macOS launchd handles both scheduling and services
            can_schedule = True
            can_manage = True
        else:
            # For other OSes, capabilities are unknown
            can_schedule = False
            can_manage = False

        return {
            "can_schedule_tasks": can_schedule,
            "can_manage_services": can_manage,
        }

    def _log_capability_warnings(self) -> None:
        """
        Log warnings if the system lacks certain capabilities.
        """
        caps = self._capabilities
        if not caps.get("can_schedule_tasks", False):
            log.warning(
                "Scheduling tasks is not supported on this operating system."
            )
        if not caps.get("can_manage_services", False):
            log.warning(
                "Managing services is not supported on this operating system."
            )

    @property
    def can_schedule_tasks(self) -> bool:
        """
        Return True if the system supports scheduling tasks.
        """
        return self._capabilities.get("can_schedule_tasks", False)

    @property
    def can_manage_services(self) -> bool:
        """
        Return True if the system supports managing services.
        """
        return self._capabilities.get("can_manage_services", False)

    # Lazy initialization of capabilities
    @property
    def _capabilities(self) -> Dict[str, bool]:
        if not hasattr(self, "_cached_capabilities"):
            self._cached_capabilities = self._check_system_capabilities()
            self._log_capability_warnings()
        return self._cached_capabilities
