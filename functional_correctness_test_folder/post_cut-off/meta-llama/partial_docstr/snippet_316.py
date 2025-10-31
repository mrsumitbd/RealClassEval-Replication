
import platform
import subprocess
from typing import Dict


class SystemMixin:
    def __init__(self, app_version: str):
        self._app_version = app_version
        self.capabilities = self._check_system_capabilities()
        self._log_capability_warnings()

    def get_app_version(self) -> str:
        '''Returns the application's version string.
        The version is typically derived from the application's settings
        during manager initialization and stored in :attr:`._app_version`.
        Returns:
            str: The application version string (e.g., "1.2.3").
        '''
        return self._app_version

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
        capabilities = {}
        if os_type == 'Linux':
            capabilities['scheduler'] = self._check_command_availability(
                'crontab')
            capabilities['service_manager'] = self._check_command_availability(
                'systemctl')
        elif os_type == 'Windows':
            capabilities['scheduler'] = self._check_command_availability(
                'schtasks')
            capabilities['service_manager'] = self._check_command_availability(
                'sc.exe')
        else:
            capabilities['scheduler'] = False
            capabilities['service_manager'] = False
        return capabilities

    def _check_command_availability(self, command: str) -> bool:
        try:
            subprocess.run([command, '--help'], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _log_capability_warnings(self) -> None:
        '''
        Internal helper to log warnings if essential system capabilities are missing.
        Called during :meth:`.__init__` after :meth:`._check_system_capabilities`.
        It inspects the :attr:`.capabilities` attribute and logs a warning message
        for each capability that is found to be unavailable. This informs the user
        that certain application features might be disabled or limited.
        '''
        import logging
        for capability, available in self.capabilities.items():
            if not available:
                logging.warning(f"Capability '{capability}' is not available.")

    @property
    def can_schedule_tasks(self) -> bool:
        return self.capabilities.get('scheduler', False)

    @property
    def can_manage_services(self) -> bool:
        return self.capabilities.get('service_manager', False)
