from typing import List
from rich.console import Group
from rich.text import Text
from rich.markup import MarkupError, escape


class ScreenBufferManager:
    """Manager for screen buffer operations and rendering."""

    def __init__(self) -> None:
        """Initialize screen buffer manager."""
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """Create Rich renderable from screen buffer.
        Args:
            screen_buffer: List of screen lines with Rich markup
        Returns:
            Rich Group renderable
        """
        renderables: list[Text] = []
        for line in screen_buffer:
            try:
                renderables.append(Text.from_markup(str(line)))
            except MarkupError:
                renderables.append(Text(escape(str(line))))
        if not renderables:
            renderables.append(Text(""))
        return Group(*renderables)
