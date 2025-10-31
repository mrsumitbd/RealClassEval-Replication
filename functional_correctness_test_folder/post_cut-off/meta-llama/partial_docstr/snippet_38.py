
from rich.console import Console
from rich.live import Live
from typing import Optional


class LiveDisplayManager:
    '''Manager for Rich Live display operations.'''

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        return Live(
            auto_refresh=auto_refresh,
            console=console or self.console,
            refresh_per_second=refresh_per_second
        )
