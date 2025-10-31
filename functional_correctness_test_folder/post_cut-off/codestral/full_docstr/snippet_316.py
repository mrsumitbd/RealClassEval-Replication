
import platform
import subprocess
from typing import Dict


class SystemMixin:
    '''
    Mixin class for BedrockServerManager that handles system information and capabilities.
    '''

    def __init__(self):
        self._app_version = None
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
        capabilities = {}
        os_type = self.get_os_type()

        if os_type == "Linux":
            capabilities['scheduler'] = self._is_command_available('crontab')
            capabilities['service_manager'] = self._is_command_available(
                'systemctl')
        elif os_type == "Windows":
            capabilities['scheduler'] = self._is_command_available('schtasks')
            capabilities['service_manager'] = self._is_command_available(
                'sc.exe')
        else:
            capabilities['scheduler'] = False
            capabilities['service_manager'] = False

        return capabilities

    def _is_command_available(self, command: str) -> bool:
        '''
        Helper method to check if a command is available in the system's PATH.
        Args:
            command (str): The command to check for.
        Returns:
            bool: True if the command is available, False otherwise.
        '''
        try:
            subprocess.run([command, '--version'], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        for capability, available in self.capabilities.items():
            if not available:
                print(
                    f"Warning: {capability} capability is not available. Some features may be limited.")

    @property
    def can_schedule_tasks(self) -> bool:
        '''bool: Indicates if a system task scheduler (``crontab`` or ``schtasks``) is available.
        This property reflects the 'scheduler' capability checked during manager
        initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to scheduled tasks (like automated backups) can be
        expected to work.
        '''
        return self.capabilities.get('scheduler', False)

    @property
    def can_manage_services(self) -> bool:
        '''bool: Indicates if a system service manager (``systemctl`` or ``sc.exe``) is available.
        This property reflects the 'service_manager' capability checked during
        manager initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to managing system services (for the Web UI or game servers)
        can be expected to work.
        '''
        return self.capabilities.get('service_manager', False)
