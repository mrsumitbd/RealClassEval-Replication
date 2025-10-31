
import platform
import shutil
import logging
from typing import Dict


class SystemMixin:
    def __init__(self, app_version: str = None):
        # Assume app_version is passed in or set elsewhere; fallback to "0.0.0"
        self._app_version = app_version if app_version is not None else "0.0.0"
        self.capabilities = self._check_system_capabilities()
        self._log_capability_warnings()

    def get_app_version(self) -> str:
        '''Returns the application's version string.'''
        return self._app_version

    def get_os_type(self) -> str:
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        os_type = self.get_os_type()
        capabilities = {}

        if os_type == "Linux":
            # Check for crontab and systemctl
            capabilities['scheduler'] = shutil.which('crontab') is not None
            capabilities['service_manager'] = shutil.which(
                'systemctl') is not None
        elif os_type == "Windows":
            # Check for schtasks and sc.exe
            capabilities['scheduler'] = shutil.which('schtasks') is not None
            capabilities['service_manager'] = shutil.which(
                'sc.exe') is not None
        else:
            # Unknown OS: assume not available
            capabilities['scheduler'] = False
            capabilities['service_manager'] = False

        return capabilities

    def _log_capability_warnings(self) -> None:
        logger = logging.getLogger(__name__)
        for cap, available in self.capabilities.items():
            if not available:
                logger.warning(
                    f"System capability '{cap}' is not available. "
                    "Some features may be disabled or limited."
                )

    @property
    def can_schedule_tasks(self) -> bool:
        return self.capabilities.get('scheduler', False)

    @property
    def can_manage_services(self) -> bool:
        return self.capabilities.get('service_manager', False)
