
from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        console = console or self.console
        return Live(console=console, auto_refresh=auto_refresh, refresh_per_second=refresh_per_second)
