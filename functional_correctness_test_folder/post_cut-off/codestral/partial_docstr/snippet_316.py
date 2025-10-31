
import platform
import subprocess
from typing import Dict


class SystemMixin:

    def __init__(self):
        self._app_version = None
        self.capabilities = self._check_system_capabilities()
        self._log_capability_warnings()

    def get_app_version(self) -> str:
        return self._app_version

    def get_os_type(self) -> str:
        return platform.system().lower()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        capabilities = {
            'scheduler': False,
            'service_manager': False
        }

        os_type = self.get_os_type()

        if os_type == 'linux':
            capabilities['scheduler'] = self._is_command_available('crontab')
            capabilities['service_manager'] = self._is_command_available(
                'systemctl')
        elif os_type == 'windows':
            capabilities['scheduler'] = self._is_command_available('schtasks')
            capabilities['service_manager'] = self._is_command_available(
                'sc.exe')

        return capabilities

    def _is_command_available(self, command: str) -> bool:
        try:
            subprocess.run([command, '--version'], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _log_capability_warnings(self) -> None:
        for capability, available in self.capabilities.items():
            if not available:
                print(
                    f"Warning: {capability} capability is not available. Some features may be limited.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self.capabilities['scheduler']

    @property
    def can_manage_services(self) -> bool:
        return self.capabilities['service_manager']
