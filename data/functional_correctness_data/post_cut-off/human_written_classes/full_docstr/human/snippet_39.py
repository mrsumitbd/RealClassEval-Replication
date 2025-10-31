from rich.console import Console, Group, RenderableType
from typing import Any, Dict, List, Optional, Tuple
from rich.text import Text

class ScreenBufferManager:
    """Manager for screen buffer operations and rendering."""

    def __init__(self) -> None:
        """Initialize screen buffer manager."""
        self.console: Optional[Console] = None

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """Create Rich renderable from screen buffer.

        Args:
            screen_buffer: List of screen lines with Rich markup

        Returns:
            Rich Group renderable
        """
        from claude_monitor.terminal.themes import get_themed_console
        if self.console is None:
            self.console = get_themed_console()
        text_objects = []
        for line in screen_buffer:
            if isinstance(line, str):
                text_obj = Text.from_markup(line)
                text_objects.append(text_obj)
            else:
                text_objects.append(line)
        return Group(*text_objects)