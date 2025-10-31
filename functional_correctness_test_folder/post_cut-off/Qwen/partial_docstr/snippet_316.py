
import platform
import subprocess
from typing import Dict


class SystemMixin:

    def __init__(self):
        self._app_version = "1.2.3"  # Example version
        self.capabilities = self._check_system_capabilities()
        self._log_capability_warnings()

    def get_app_version(self) -> str:
        return self._app_version

    def get_os_type(self) -> str:
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        capabilities = {
            'scheduler': self._check_utility('crontab' if self.get_os_type() == 'Linux' else 'schtasks'),
            'service_manager': self._check_utility('systemctl' if self.get_os_type() == 'Linux' else 'sc.exe')
        }
        return capabilities

    def _check_utility(self, utility: str) -> bool:
        try:
            subprocess.run([utility], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def _log_capability_warnings(self) -> None:
        for capability, available in self.capabilities.items():
            if not available:
                print(
                    f"Warning: {capability} is not available. Some features may be limited.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self.capabilities.get('scheduler', False)

    @property
    def can_manage_services(self) -> bool:
        return self.capabilities.get('service_manager', False)
