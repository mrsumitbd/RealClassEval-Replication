from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    def __init__(self) -> None:
        '''Initialize screen buffer manager.'''
        self._last_screen: List[str] = []

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        '''Create Rich renderable from screen buffer.
        Args:
            screen_buffer: List of screen lines with Rich markup
        Returns:
            Rich Group renderable
        '''
        if screen_buffer is None:
            screen_buffer = []
        self._last_screen = list(screen_buffer)

        text = Text()
        for i, line in enumerate(screen_buffer):
            text.append_text(Text.from_markup(line))
            if i < len(screen_buffer) - 1:
                text.append("\n")

        return Group(text)
