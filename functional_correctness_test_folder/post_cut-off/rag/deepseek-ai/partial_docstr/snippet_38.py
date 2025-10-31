
from rich.console import Console
from rich.live import Live
from typing import Optional


class LiveDisplayManager:
    '''Manager for Rich Live display operations.'''

    def __init__(self, console: Optional[Console] = None) -> None:
        '''Initialize live display manager.
        Args:
            console: Optional Rich console instance
        '''
        self.console = console

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        '''Create Rich Live display context.
        Args:
            auto_refresh: Whether to auto-refresh
            console: Optional console instance
            refresh_per_second: Display refresh rate (0.1-20 Hz)
        Returns:
            Rich Live context manager
        '''
        console = console or self.console or Console()
        return Live(
            console=console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second
        )
