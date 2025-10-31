from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    '''Manager for screen buffer operations and rendering.'''

    def __init__(self) -> None:
        '''Initialize screen buffer manager.'''
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        '''Create Rich renderable from screen buffer.
        Args:
            screen_buffer: List of screen lines with Rich markup
        Returns:
            Rich Group renderable
        '''
        if not isinstance(screen_buffer, list):
            raise TypeError("screen_buffer must be a list of strings")
        renderables = []
        for line in screen_buffer:
            if not isinstance(line, str):
                line = str(line)
            renderables.append(Text.from_markup(line))
        return Group(*renderables)
