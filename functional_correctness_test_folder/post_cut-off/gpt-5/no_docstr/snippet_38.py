from typing import Optional

try:
    from rich.console import Console
    from rich.live import Live
except Exception as e:
    raise ImportError(
        "rich is required for LiveDisplayManager. Please install it with `pip install rich`.") from e


class LiveDisplayManager:

    def __init__(self, console: Optional[Console] = None) -> None:
        self.console: Console = console if console is not None else Console()

    def create_live_display(
        self,
        auto_refresh: bool = True,
        console: Optional[Console] = None,
        refresh_per_second: float = 0.75
    ) -> Live:
        target_console = console if console is not None else self.console
        return Live(
            console=target_console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
        )
