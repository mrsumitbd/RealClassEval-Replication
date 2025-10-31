from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:
    '''Manager for Rich Live display operations.'''

    def __init__(self, console: Optional[Console] = None) -> None:
        '''Initialize live display manager.
        Args:
            console: Optional Rich console instance
        '''
        self.console: Console = console or Console()

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        '''Create Rich Live display context.
        Args:
            auto_refresh: Whether to auto-refresh
            console: Optional console instance
            refresh_per_second: Display refresh rate (0.1-20 Hz)
        Returns:
            Rich Live context manager
        '''
        if not isinstance(refresh_per_second, (int, float)):
            raise TypeError('refresh_per_second must be a number')
        if refresh_per_second < 0.1 or refresh_per_second > 20:
            raise ValueError(
                'refresh_per_second must be between 0.1 and 20 Hz')
        use_console = console or self.console or Console()
        return Live(
            console=use_console,
            auto_refresh=auto_refresh,
            refresh_per_second=float(refresh_per_second),
        )
