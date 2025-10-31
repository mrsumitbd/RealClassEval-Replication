
import platform
import sys
from typing import Dict


class SystemMixin:

    def get_app_version(self) -> str:
        # Simulate an application version
        return "1.0.0"

    def get_os_type(self) -> str:
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        os_type = self.get_os_type()
        capabilities = {
            "can_schedule_tasks": os_type in ("Linux", "Darwin", "Windows"),
            "can_manage_services": os_type in ("Linux", "Darwin"),
        }
        return capabilities

    def _log_capability_warnings(self) -> None:
        caps = self._check_system_capabilities()
        if not caps["can_schedule_tasks"]:
            print("Warning: Task scheduling is not supported on this OS.")
        if not caps["can_manage_services"]:
            print("Warning: Service management is not supported on this OS.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self._check_system_capabilities()["can_schedule_tasks"]

    @property
    def can_manage_services(self) -> bool:
        return self._check_system_capabilities()["can_manage_services"]
