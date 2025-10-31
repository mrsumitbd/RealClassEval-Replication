
from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:
    '''Manager for Rich Live display operations.'''

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console if console is not None else Console()

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        live_console = console if console is not None else self.console
        return Live(auto_refresh=auto_refresh, console=live_console, refresh_per_second=refresh_per_second)
