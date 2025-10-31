
import platform
from typing import Dict


class SystemMixin:

    def get_app_version(self) -> str:
        return "1.0.0"

    def get_os_type(self) -> str:
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        capabilities = {
            'can_schedule_tasks': True,
            'can_manage_services': True
        }
        return capabilities

    def _log_capability_warnings(self) -> None:
        capabilities = self._check_system_capabilities()
        if not capabilities['can_schedule_tasks']:
            print("Warning: Task scheduling is not supported on this system.")
        if not capabilities['can_manage_services']:
            print("Warning: Service management is not supported on this system.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self._check_system_capabilities()['can_schedule_tasks']

    @property
    def can_manage_services(self) -> bool:
        return self._check_system_capabilities()['can_manage_services']
