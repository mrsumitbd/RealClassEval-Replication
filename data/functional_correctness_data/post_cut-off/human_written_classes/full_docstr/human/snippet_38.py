from rich.console import Console, Group, RenderableType
from typing import Any, Dict, List, Optional, Tuple
from rich.live import Live

class LiveDisplayManager:
    """Manager for Rich Live display operations."""

    def __init__(self, console: Optional[Console]=None) -> None:
        """Initialize live display manager.

        Args:
            console: Optional Rich console instance
        """
        self._console = console
        self._live_context: Optional[Live] = None
        self._current_renderable: Optional[RenderableType] = None

    def create_live_display(self, auto_refresh: bool=True, console: Optional[Console]=None, refresh_per_second: float=0.75) -> Live:
        """Create Rich Live display context.

        Args:
            auto_refresh: Whether to auto-refresh
            console: Optional console instance
            refresh_per_second: Display refresh rate (0.1-20 Hz)

        Returns:
            Rich Live context manager
        """
        display_console = console or self._console
        self._live_context = Live(console=display_console, refresh_per_second=refresh_per_second, auto_refresh=auto_refresh, vertical_overflow='visible')
        return self._live_context