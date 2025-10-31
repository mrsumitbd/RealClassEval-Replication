
import logging
import platform
import shutil
from typing import Dict

logger = logging.getLogger(__name__)


class SystemMixin:
    """
    Mixin that provides system‑level information and capability checks.
    """

    def __init__(self, app_version: str):
        """
        Initialise the mixin.

        Parameters
        ----------
        app_version : str
            The application version string (e.g., "1.2.3").
        """
        self._app_version: str = app_version
        self.capabilities: Dict[str, bool] = self._check_system_capabilities()
        self._log_capability_warnings()

    def get_app_version(self) -> str:
        """Return the application version string."""
        return self._app_version

    def get_os_type(self) -> str:
        """Return the operating system type (e.g., 'Linux', 'Windows')."""
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        """
        Check for the availability of external OS‑level dependencies.

        Returns
        -------
        Dict[str, bool]
            Mapping of capability names to booleans indicating presence.
        """
        os_type = self.get_os_type()
        capabilities: Dict[str, bool] = {}

        # Scheduler
        if os_type == "Linux":
            capabilities["scheduler"] = shutil.which("crontab") is not None
        elif os_type == "Windows":
            capabilities["scheduler"] = shutil.which("schtasks") is not None
        else:
            capabilities["scheduler"] = False

        # Service manager
        if os_type == "Linux":
            capabilities["service_manager"] = shutil.which(
                "systemctl") is not None
        elif os_type == "Windows":
            # On Windows the command is typically 'sc' (sc.exe is the executable)
            capabilities["service_manager"] = shutil.which("sc") is not None
        else:
            capabilities["service_manager"] = False

        return capabilities

    def _log_capability_warnings(self) -> None:
        """
        Log warnings for any missing essential system capabilities.
        """
        for name, available in self.capabilities.items():
            if not available:
                logger.warning(
                    f"Essential system capability '{name}' is not available. "
                    f"Related features may be disabled."
                )

    @property
    def can_schedule_tasks(self) -> bool:
        """Return True if the system supports task scheduling."""
        return self.capabilities.get("scheduler", False)

    @property
    def can_manage_services(self) -> bool:
        """Return True if the system supports service management."""
        return self.capabilities.get("service_manager", False)
