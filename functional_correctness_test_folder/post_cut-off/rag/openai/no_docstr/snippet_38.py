
from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.live import Live


class LiveDisplayManager:
    """Manager for Rich Live display operations."""

    def __init__(self, console: Optional[Console] = None) -> None:
        """
        Initialize live display manager.

        Args:
            console: Optional Rich console instance.
        """
        self.console: Console = console or Console()
        self._live: Optional[Live] = None

    def create_live_display(
        self,
        auto_refresh: bool = True,
        console: Optional[Console] = None,
        refresh_per_second: float = 0.75,
    ) -> Live:
        """
        Create Rich Live display context.

        Args:
            auto_refresh: Whether to auto-refresh.
            console: Optional console instance.
            refresh_per_second: Display refresh rate (0.1-20 Hz).

        Returns:
            Rich Live context manager.
        """
        # Use the provided console or fall back to the manager's console.
        target_console = console or self.console

        # Clamp refresh rate to a reasonable range.
        if refresh_per_second < 0.1:
            refresh_per_second = 0.1
        elif refresh_per_second > 20.0:
            refresh_per_second = 20.0

        self._live = Live(
            auto_refresh=auto_refresh,
            console=target_console,
            refresh_per_second=refresh_per_second,
        )
        return self._live
