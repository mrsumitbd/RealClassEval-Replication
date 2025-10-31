
import platform
import shutil
import logging
from typing import Dict


class SystemMixin:
    '''
    Mixin class for BedrockServerManager that handles system information and capabilities.
    '''

    def get_app_version(self) -> str:
        '''Returns the application's version string.'''
        return getattr(self, "_app_version", "unknown")

    def get_os_type(self) -> str:
        '''Returns the current operating system type string.'''
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        '''
        Internal helper to check for the availability of external OS-level
        dependencies and report their status.
        '''
        os_type = self.get_os_type()
        capabilities = {}

        if os_type == "Linux":
            # Scheduler: crontab
            capabilities['scheduler'] = shutil.which("crontab") is not None
            # Service manager: systemctl
            capabilities['service_manager'] = shutil.which(
                "systemctl") is not None
        elif os_type == "Windows":
            # Scheduler: schtasks
            capabilities['scheduler'] = shutil.which("schtasks") is not None
            # Service manager: sc.exe
            capabilities['service_manager'] = shutil.which(
                "sc.exe") is not None
        elif os_type == "Darwin":
            # macOS: crontab for scheduler, launchctl for service manager (optional)
            capabilities['scheduler'] = shutil.which("crontab") is not None
            # macOS doesn't use systemctl or sc.exe, but launchctl is the closest
            capabilities['service_manager'] = shutil.which(
                "launchctl") is not None
        else:
            # Unknown OS: assume nothing is available
            capabilities['scheduler'] = False
            capabilities['service_manager'] = False

        self.capabilities = capabilities
        return capabilities

    def _log_capability_warnings(self) -> None:
        '''
        Internal helper to log warnings if essential system capabilities are missing.
        '''
        logger = getattr(self, "logger", None)
        if logger is None:
            logger = logging.getLogger(__name__)

        caps = getattr(self, "capabilities", {})
        if not caps:
            return

        if not caps.get("scheduler", False):
            logger.warning(
                "System task scheduler (crontab/schtasks) not found. Scheduled tasks will be unavailable.")
        if not caps.get("service_manager", False):
            logger.warning(
                "System service manager (systemctl/sc.exe/launchctl) not found. Service management features will be unavailable.")

    @property
    def can_schedule_tasks(self) -> bool:
        '''bool: Indicates if a system task scheduler is available.'''
        return getattr(self, "capabilities", {}).get("scheduler", False)

    @property
    def can_manage_services(self) -> bool:
        '''bool: Indicates if a system service manager is available.'''
        return getattr(self, "capabilities", {}).get("service_manager", False)
