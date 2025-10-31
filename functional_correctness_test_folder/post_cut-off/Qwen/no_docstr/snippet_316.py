
from typing import Dict


class SystemMixin:

    def get_app_version(self) -> str:
        return "1.0.0"

    def get_os_type(self) -> str:
        return "Linux"

    def _check_system_capabilities(self) -> Dict[str, bool]:
        return {
            "can_schedule_tasks": True,
            "can_manage_services": True
        }

    def _log_capability_warnings(self) -> None:
        print("No capability warnings to log.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self._check_system_capabilities().get("can_schedule_tasks", False)

    @property
    def can_manage_services(self) -> bool:
        return self._check_system_capabilities().get("can_manage_services", False)
