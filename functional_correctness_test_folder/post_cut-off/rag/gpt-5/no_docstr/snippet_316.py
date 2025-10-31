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
        return str(getattr(self, '_app_version', '') or '')

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

        if os_type == 'Windows':
            scheduler_candidates = ('schtasks', 'schtasks.exe')
            service_manager_candidates = ('sc.exe', 'sc')
        else:
            scheduler_candidates = ('crontab',)
            service_manager_candidates = ('systemctl',)

        def _has_any(candidates) -> bool:
            return any(shutil.which(name) is not None for name in candidates)

        caps = {
            'scheduler': _has_any(scheduler_candidates),
            'service_manager': _has_any(service_manager_candidates),
        }
        self.capabilities = caps
        return caps

    def _log_capability_warnings(self) -> None:
        '''
        Internal helper to log warnings if essential system capabilities are missing.
        Called during :meth:`.__init__` after :meth:`._check_system_capabilities`.
        It inspects the :attr:`.capabilities` attribute and logs a warning message
        for each capability that is found to be unavailable. This informs the user
        that certain application features might be disabled or limited.
        '''
        logger = getattr(self, 'logger', logging.getLogger(__name__))
        caps = getattr(self, 'capabilities', {}) or {}

        os_type = self.get_os_type()
        if os_type == 'Windows':
            scheduler_hint = 'schtasks'
            service_hint = 'sc.exe'
        else:
            scheduler_hint = 'crontab'
            service_hint = 'systemctl'

        if not caps.get('scheduler', False):
            logger.warning(
                f"System capability missing: scheduler not found. "
                f"Expected '{scheduler_hint}' to be available. "
                "Features that rely on scheduled tasks may be limited."
            )

        if not caps.get('service_manager', False):
            logger.warning(
                f"System capability missing: service manager not found. "
                f"Expected '{service_hint}' to be available. "
                "Features that manage system services may be limited."
            )

    @property
    def can_schedule_tasks(self) -> bool:
        '''bool: Indicates if a system task scheduler (``crontab`` or ``schtasks``) is available.
        This property reflects the 'scheduler' capability checked during manager
        initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to scheduled tasks (like automated backups) can be
        expected to work.
        '''
        return bool(getattr(self, 'capabilities', {}).get('scheduler', False))

    @property
    def can_manage_services(self) -> bool:
        '''bool: Indicates if a system service manager (``systemctl`` or ``sc.exe``) is available.
        This property reflects the 'service_manager' capability checked during
        manager initialization by :meth:`._check_system_capabilities`. If ``True``,
        features related to managing system services (for the Web UI or game servers)
        can be expected to work.
        '''
        return bool(getattr(self, 'capabilities', {}).get('service_manager', False))
