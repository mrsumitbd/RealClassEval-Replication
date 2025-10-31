from typing import Dict
import platform
import shutil
import logging


class SystemMixin:

    def get_app_version(self) -> str:
        '''Returns the application's version string.
        The version is typically derived from the application's settings
        during manager initialization and stored in :attr:`._app_version`.
        Returns:
            str: The application version string (e.g., "1.2.3").
        '''
        val = getattr(self, "_app_version", "")
        return str(val) if val is not None else ""

    def get_os_type(self) -> str:

        return platform.system()

    def _check_system_capabilities(self) -> Dict[str, bool]:
        '''
        Internal helper to check for the availability of external OS-level
        dependencies and report their status.
        This method is called during :meth:`.__init__` to determine if optional
        system utilities, required for certain features, are present.
        Currently, it checks for:
            - 'scheduler': ``crontab`` (Linux) or ``schtasks`` (Windows).
            - 'service_manager': ``systemctl`` (Linux) or ``sc.exe`` (Windows).
        The results are stored in the :attr:`.capabilities` dictionary.
        Returns:
            Dict[str, bool]: A dictionary where keys are capability names
            (e.g., "scheduler", "service_manager") and values are booleans
            indicating if the corresponding utility was found.
        '''
        os_type = self.get_os_type()
        scheduler_cmd = None
        service_cmds = []

        if os_type == "Linux":
            scheduler_cmd = "crontab"
            service_cmds = ["systemctl"]
        elif os_type == "Windows":
            scheduler_cmd = "schtasks"
            # shutil.which('sc') typically finds sc.exe on PATH
            service_cmds = ["sc", "sc.exe"]
        else:
            scheduler_cmd = None
            service_cmds = []

        scheduler_available = False
        if scheduler_cmd:
            scheduler_available = shutil.which(scheduler_cmd) is not None

        service_available = any(shutil.which(
            cmd) is not None for cmd in service_cmds) if service_cmds else False

        caps = {
            "scheduler": scheduler_available,
            "service_manager": service_available,
        }
        setattr(self, "capabilities", caps)
        return caps

    def _log_capability_warnings(self) -> None:
        '''
        Internal helper to log warnings if essential system capabilities are missing.
        Called during :meth:`.__init__` after :meth:`._check_system_capabilities`.
        It inspects the :attr:`.capabilities` attribute and logs a warning message
        for each capability that is found to be unavailable. This informs the user
        that certain application features might be disabled or limited.
        '''
        logger = logging.getLogger(__name__)
        caps = getattr(self, "capabilities", None)
        if not isinstance(caps, dict):
            caps = self._check_system_capabilities()

        if not caps.get("scheduler", False):
            logger.warning(
                "System capability missing: scheduler utility not found. Task scheduling features may be unavailable.")
        if not caps.get("service_manager", False):
            logger.warning(
                "System capability missing: service manager utility not found. Service management features may be unavailable.")

    @property
    def can_schedule_tasks(self) -> bool:

        caps = getattr(self, "capabilities", None)
        if not isinstance(caps, dict):
            caps = self._check_system_capabilities()
        return bool(caps.get("scheduler", False))

    @property
    def can_manage_services(self) -> bool:

        caps = getattr(self, "capabilities", None)
        if not isinstance(caps, dict):
            caps = self._check_system_capabilities()
        return bool(caps.get("service_manager", False))
