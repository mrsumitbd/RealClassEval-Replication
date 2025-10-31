from ii_agent.utils.constants import WorkSpaceMode
from ii_agent.utils.tool_client.manager import SessionResult, PexpectSessionManager
from ii_agent.core.storage.models.settings import Settings

class TerminalClient:
    """Factory class for creating the appropriate client based on configuration."""

    def __init__(self, settings: Settings):
        self.config = settings.client_config
        if settings.sandbox_config.mode == WorkSpaceMode.LOCAL:
            self._client = LocalTerminalClient(self.config)
        elif settings.sandbox_config.mode == WorkSpaceMode.E2B or settings.sandbox_config.mode == WorkSpaceMode.DOCKER:
            self._client = RemoteTerminalClient(self.config)
        else:
            raise ValueError(f"Unsupported mode: {self.config.mode}. Must be 'local' or 'remote' or 'e2b'")

    def create_session(self, session_id: str) -> SessionResult:
        """Create a new terminal session."""
        return self._client.create_session(session_id)

    def shell_exec(self, session_id: str, command: str, exec_dir: str=None, timeout: int=30, **kwargs) -> SessionResult:
        """Execute a shell command in a session."""
        return self._client.shell_exec(session_id, command, exec_dir, timeout, **kwargs)

    def shell_view(self, session_id: str) -> SessionResult:
        """Get current view of a shell session."""
        return self._client.shell_view(session_id)

    def shell_wait(self, session_id: str, seconds: int=30) -> SessionResult:
        """Wait for a shell session to complete current command."""
        return self._client.shell_wait(session_id, seconds)

    def shell_write_to_process(self, session_id: str, input_text: str, press_enter: bool=False) -> SessionResult:
        """Write text to a running process in a shell session."""
        return self._client.shell_write_to_process(session_id, input_text, press_enter)

    def shell_kill_process(self, session_id: str) -> SessionResult:
        """Kill the process in a shell session."""
        return self._client.shell_kill_process(session_id)