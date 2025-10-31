
from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    def __init__(self) -> None:
        """Initialize screen buffer manager."""
        # No internal state needed for this simple implementation
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """
        Create Rich renderable from screen buffer.

        Args:
            screen_buffer: List of screen lines with Rich markup

        Returns:
            Rich Group renderable
        """
        # Convert each line into a Rich Text object and group them
        return Group(*[Text(line) for line in screen_buffer])
