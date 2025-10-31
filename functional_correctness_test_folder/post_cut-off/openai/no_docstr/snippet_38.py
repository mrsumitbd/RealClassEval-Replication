
from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:
    """
    A simple manager for Rich Live displays.
    """

    def __init__(self, console: Optional[Console] = None) -> None:
        """
        Initialize the manager with an optional Console.
        If no console is provided, a default Console will be created.
        """
        self.console: Console = console or Console()

    def create_live_display(
        self,
        auto_refresh: bool = True,
        console: Optional[Console] = None,
        refresh_per_second: float = 0.75,
    ) -> Live:
        """
        Create and return a Rich Live object.

        Parameters
        ----------
        auto_refresh : bool, optional
            Whether the Live display should automatically refresh.
        console : Optional[Console], optional
            Console to use for the Live display. If None, the manager's console is used.
        refresh_per_second : float, optional
            The refresh rate for the Live display.

        Returns
        -------
        Live
            A Rich Live object configured with the provided parameters.
        """
        target_console = console or self.console
        return Live(
            auto_refresh=auto_refresh,
            console=target_console,
            refresh_per_second=refresh_per_second,
        )
