
from typing import Sequence, List


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self._width: int = 0
        self._height: int = 0
        self._left: int = 0
        self._right: int = 0
        self._top: int = 0
        self._bottom: int = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
        if width <= 0 or height <= 0:
            raise ValueError("Screen dimensions must be positive integers.")
        self._width = width
        self._height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        '''Set screen margins.
        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        '''
        if any(m < 0 for m in (left, right, top, bottom)):
            raise ValueError("Margins must be non‑negative.")
        if left + right >= self._width:
            raise ValueError("Left and right margins exceed screen width.")
        if top + bottom >= self._height:
            raise ValueError("Top and bottom margins exceed screen height.")
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> List[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        if self._width == 0 or self._height == 0:
            raise RuntimeError(
                "Screen dimensions must be set before creating layout.")

        inner_width = self._width - self._left - self._right
        inner_height = self._height - self._top - self._bottom

        # Prepare the content lines
        content_lines: List[str] = []

        for section in content_sections:
            for line in section:
                # Truncate or pad the line to fit the inner width
                trimmed = line[:inner_width]
                padded = trimmed.ljust(inner_width)
                # Add left and right margins
                full_line = ' ' * self._left + padded + ' ' * self._right
                content_lines.append(full_line)

        # Truncate or pad to fit the inner height
        if len(content_lines) > inner_height:
            content_lines = content_lines[:inner_height]
        else:
            empty_line = ' ' * self._width
            content_lines.extend(
                [empty_line] * (inner_height - len(content_lines)))

        # Add top and bottom margins
        top_margin = [' ' * self._width] * self._top
        bottom_margin = [' ' * self._width] * self._bottom

        full_layout = top_margin + content_lines + bottom_margin
        return full_layout
