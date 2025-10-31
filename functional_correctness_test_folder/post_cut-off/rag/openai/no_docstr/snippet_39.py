
from typing import List
from rich.console import Group


class ScreenBufferManager:
    '''Manager for screen buffer operations and rendering.'''

    def __init__(self) -> None:
        '''Initialize screen buffer manager.'''
        # No internal state required for this simple implementation
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        '''Create Rich renderable from screen buffer.
        Args:
            screen_buffer: List of screen lines with Rich markup
        Returns:
            Rich Group renderable
        '''
        # Rich's Group can accept plain strings (with markup) directly.
        # Each element will be rendered on its own line.
        return Group(*screen_buffer)
