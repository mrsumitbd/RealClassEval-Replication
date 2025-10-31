
import platform
import sys
from typing import Dict


class SystemMixin:

    def get_app_version(self) -> str:
        return "1.0.0"

    def get_os_type(self) -> str:
        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        capabilities = {
            "can_schedule_tasks": self.can_schedule_tasks,
            "can_manage_services": self.can_manage_services
        }
        return capabilities

    def _log_capability_warnings(self) -> None:
        capabilities = self._check_system_capabilities()
        for capability, is_supported in capabilities.items():
            if not is_supported:
                print(
                    f"Warning: {capability} is not supported on this system.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self.get_os_type().lower() in ["windows", "linux"]

    @property
    def can_manage_services(self) -> bool:
        return self.get_os_type().lower() == "windows"
