
from __future__ import annotations
from typing import Sequence, List


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width: int = 80
        self.height: int = 24
        self.left: int = 0
        self.right: int = 0
        self.top: int = 0
        self.bottom: int = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
        if width <= 0 or height <= 0:
            raise ValueError(
                'Screen width and height must be positive integers.')
        self.width = width
        self.height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        '''Set screen margins.
        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        '''
        for name, value in (('left', left), ('right', right), ('top', top), ('bottom', bottom)):
            if value < 0:
                raise ValueError(f'{name} margin must be non‑negative.')
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def _wrap_line(self, line: str, width: int) -> List[str]:
        '''Wrap a single line into chunks of at most `width` characters.'''
        chunks: List[str] = []
        while len(line) > width:
            chunks.append(line[:width])
            line = line[width:]
        chunks.append(line)
        return chunks

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> List[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        avail_width = self.width - self.left - self.right
        avail_height = self.height - self.top - self.bottom

        if avail_width <= 0 or avail_height <= 0:
            raise ValueError(
                'Available width and height must be positive after applying margins.')

        # Build the body of the screen
        body: List[str] = []

        for section in content_sections:
            for raw_line in section:
                # Wrap the line if necessary
                wrapped = self._wrap_line(raw_line, avail_width)
                for chunk in wrapped:
                    # Pad left and right margins
                    padded = (' ' * self.left) + \
                        chunk.ljust(avail_width) + (' ' * self.right)
                    body.append(padded)

        # Truncate if body exceeds available height
        if len(body) > avail_height:
            body = body[:avail_height]

        # Add top and bottom margins
        top_margin = [' ' * self.width] * self.top
        bottom_margin = [' ' * self.width] * self.bottom

        return top_margin + body + bottom_margin
