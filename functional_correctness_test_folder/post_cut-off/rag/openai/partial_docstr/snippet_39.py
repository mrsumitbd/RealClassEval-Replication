
from __future__ import annotations

from typing import List

from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    """Manager for screen buffer operations and rendering."""

    def __init__(self) -> None:
        """Initialize screen buffer manager."""
        # The buffer holds the raw lines (with Rich markup) that will be rendered.
        self._buffer: List[str] = []

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """
        Create a Rich renderable from a screen buffer.

        Parameters
        ----------
        screen_buffer
            List of screen lines with Rich markup.

        Returns
        -------
        Group
            A Rich Group renderable that can be printed to a console.
        """
        # Convert each line into a Rich Text object so that markup is interpreted.
        # If the buffer is empty, return an empty Group to avoid rendering errors.
        if not screen_buffer:
            return Group()

        return Group(*[Text(line) for line in screen_buffer])
