
import logging
import platform
import shutil
from typing import Dict


class SystemMixin:
    """
    Mixin class for BedrockServerManager that handles system information and capabilities.
    """

    def get_app_version(self) -> str:
        """Returns the application's version string."""
        return getattr(self, "_app_version", "unknown")

    def get_os_type(self) -> str:
        """Returns the current operating system type string."""
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        """
        Internal helper to check for the availability of external OS-level
        dependencies and report their status.
        """
        os_type = self.get_os_type()
        capabilities: Dict[str, bool] = {}

        # Scheduler
        if os_type == "Linux":
            scheduler_cmd = "crontab"
        elif os_type == "Windows":
            scheduler_cmd = "schtasks"
        else:
            scheduler_cmd = None

        capabilities["scheduler"] = bool(
            scheduler_cmd and shutil.which(scheduler_cmd)
        )

        # Service manager
        if os_type == "Linux":
            service_cmd = "systemctl"
        elif os_type == "Windows":
            service_cmd = "sc.exe"
        else:
            service_cmd = None

        capabilities["service_manager"] = bool(
            service_cmd and shutil.which(service_cmd)
        )

        # Store the capabilities for later use
        self.capabilities = capabilities
        return capabilities

    def _log_capability_warnings(self) -> None:
        """
        Internal helper to log warnings if essential system capabilities are missing.
        """
        if not hasattr(self, "capabilities"):
            return

        for name, available in self.capabilities.items():
            if not available:
                logging.warning(
                    f"System capability '{name}' is not available; "
                    f"related features may be disabled."
                )

    @property
    def can_schedule_tasks(self) -> bool:
        """Indicates if a system task scheduler is available."""
        return getattr(self, "capabilities", {}).get("scheduler", False)

    @property
    def can_manage_services(self) -> bool:
        """Indicates if a system service manager is available."""
        return getattr(self, "capabilities", {}).get("service_manager", False)
