
from rich.console import Group
from rich.text import Text
from typing import List


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
        renderables = [Text(line) for line in screen_buffer]
        return Group(*renderables)
