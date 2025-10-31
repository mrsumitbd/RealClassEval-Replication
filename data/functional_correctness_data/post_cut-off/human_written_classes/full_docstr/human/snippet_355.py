from streetrace.app_state import AppState
from rich.console import Console
from types import TracebackType

class StatusSpinner:
    """Console Status, encapsulates rich.status."""
    _ICON = 'hamburger'
    _EMPTY_MESSAGE = 'Working...'

    def __init__(self, app_state: AppState, console: Console) -> None:
        """Initialize the instance and instantiate rich.status.

        Args:
            app_state: App State container.
            console: The console instance to attach the spinner to.

        """
        self.app_state = app_state
        self.console = console
        self._status: Status | None = None

    def update_state(self) -> None:
        """Update status message."""
        if self._status:
            self._status.update(_format_app_state_str(_STATUS_MESSAGE_TEMPLATE, self.app_state))

    def __enter__(self) -> 'StatusSpinner':
        """Enter the context by starting the spinner.

        Returns:
            self, so that logging methods can be called within the context.

        """
        self._status = self.console.status(status=StatusSpinner._EMPTY_MESSAGE, spinner=StatusSpinner._ICON).__enter__()
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the context by propagating the signal to the spinner.

        Args:
            exc_type: The type of exception raised (if any).
            exc_value: The exception instance (if any).
            traceback: The traceback object (if any).

        """
        if self._status:
            self._status.__exit__(exc_type, exc_value, traceback)
            self._status = None