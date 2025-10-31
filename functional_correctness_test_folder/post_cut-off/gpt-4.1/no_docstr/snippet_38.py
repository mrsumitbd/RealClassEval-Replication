
from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:

    def __init__(self, console: Optional[Console] = None) -> None:
        if console is None:
            self.console = Console()
        else:
            self.console = console

    def create_live_display(self, auto_refresh: bool = True, console: Optional[Console] = None, refresh_per_second: float = 0.75) -> Live:
        use_console = console if console is not None else self.console
        return Live(
            renderable="",
            console=use_console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second
        )
