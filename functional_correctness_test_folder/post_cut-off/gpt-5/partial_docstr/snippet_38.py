from typing import Optional
from rich.console import Console
from rich.live import Live


class LiveDisplayManager:
    '''Manager for Rich Live display operations.'''

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console: Console = console if console is not None else Console()

    def create_live_display(
        self,
        auto_refresh: bool = True,
        console: Optional[Console] = None,
        refresh_per_second: float = 0.75
    ) -> Live:
        target_console = console if console is not None else self.console
        if refresh_per_second <= 0:
            refresh_per_second = 0.75
        return Live(
            console=target_console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
        )
