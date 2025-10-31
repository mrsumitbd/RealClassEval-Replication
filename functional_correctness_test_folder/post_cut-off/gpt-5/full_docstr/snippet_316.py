from typing import Dict
import platform
import shutil
import logging


class SystemMixin:
    '''
    Mixin class for BedrockServerManager that handles system information and capabilities.
        '''

    def get_app_version(self) -> str:
        '''Returns the application's version string.
        The version is typically derived from the application's settings
        during manager initialization and stored in :attr:`._app_version`.
        Returns:
            str: The application version string (e.g., "1.2.3").
        '''
        return str(getattr(self, "_app_version", "unknown"))

    def get_os_type(self) -> str:
        '''Returns the current operating system type string.
        This method uses :func:`platform.system()` to determine the OS.
        Common return values include "Linux", "Windows", "Darwin" (for macOS).
        Returns:
            str: A string representing the current operating system.
        '''
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

        if os_type == "Linux":
            scheduler_cmds = ["crontab"]
            service_cmds = ["systemctl"]
        elif os_type == "Windows":
            scheduler_cmds = ["schtasks", "schtasks.exe"]
            service_cmds = ["sc", "sc.exe"]
        else:
            scheduler_cmds = []
            service_cmds = []

        def has_command(cmds):
            for c in cmds:
                if shutil.which(c):
                    return True
            return False

        capabilities = {
            "scheduler": has_command(scheduler_cmds),
            "service_manager": has_command(service_cmds),
        }

        self.capabilities = capabilities
        return capabilities

    def _log_capability_warnings(self) -> None:
        '''
        Internal helper to log warnings if essential system capabilities are missing.
        Called during :meth:`.__init__` after :meth:`._check_system_capabilities`.
        It inspects the :attr:`.capabilities` attribute and logs a warning message
        for each capability that is found to be unavailable. This informs the user
        that certain application features might be disabled or limited.
        '''
        logger = getattr(self, "logger", logging.getLogger(__name__))
        capabilities = getattr(self, "capabilities", None)
        if capabilities is None:
            capabilities = self._check_system_capabilities()

        warnings = {
            "scheduler": "System task scheduler not found (crontab/schtasks). Scheduled features may be unavailable.",
            "service_manager": "System service manager not found (systemctl/sc.exe). Service management features may be unavailable.",
        }

        for cap, available in capabilities.items():
            if not available and cap in warnings:
                logger.warning(warnings[cap])

    @property
    def can_schedule_tasks(self) -> bool:
        '''bool: Indicates if a system task scheduler (``crontab`` or ``schtasks``) is available.
        This property reflects the 'scheduler' capability checked during manager
        initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to scheduled tasks (like automated backups) can be
        expected to work.
        '''
        if not hasattr(self, "capabilities"):
            self._check_system_capabilities()
        return bool(self.capabilities.get("scheduler", False))

    @property
    def can_manage_services(self) -> bool:
        '''bool: Indicates if a system service manager (``systemctl`` or ``sc.exe``) is available.
        This property reflects the 'service_manager' capability checked during
        manager initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to managing system services (for the Web UI or game servers)
        can be expected to work.
        '''
        if not hasattr(self, "capabilities"):
            self._check_system_capabilities()
        return bool(self.capabilities.get("service_manager", False))
