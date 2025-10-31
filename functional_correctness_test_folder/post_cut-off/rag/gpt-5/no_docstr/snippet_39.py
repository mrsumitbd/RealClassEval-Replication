from typing import List, Optional, Tuple
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    '''Manager for screen buffer operations and rendering.'''

    def __init__(self) -> None:
        '''Initialize screen buffer manager.'''
        self._last_buffer: Optional[Tuple[str, ...]] = None
        self._last_group: Optional[Group] = None

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        '''Create Rich renderable from screen buffer.
        Args:
            screen_buffer: List of screen lines with Rich markup
        Returns:
            Rich Group renderable
        '''
        if not screen_buffer:
            return Group()

        normalized = tuple((line.rstrip('\n') if isinstance(
            line, str) else str(line)) for line in screen_buffer)

        if self._last_buffer == normalized and self._last_group is not None:
            return self._last_group

        combined = '\n'.join(normalized)
        text = Text.from_markup(combined, emoji=True)
        group = Group(text)

        self._last_buffer = normalized
        self._last_group = group
        return group
