
from typing import Sequence


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 0
        self.height = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
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
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        content_width = max(0, self.width - self.left - self.right)
        content_height = max(0, self.height - self.top - self.bottom)
        layout = []

        # Prepare all content lines
        all_content_lines = []
        for section in content_sections:
            all_content_lines.extend(section)
        # Truncate or pad content lines to fit content_height
        if len(all_content_lines) > content_height:
            all_content_lines = all_content_lines[:content_height]
        else:
            all_content_lines += [''] * \
                (content_height - len(all_content_lines))

        # Pad each line to content_width
        content_lines = []
        for line in all_content_lines:
            if len(line) > content_width:
                content_lines.append(line[:content_width])
            else:
                content_lines.append(line.ljust(content_width))

        # Top margin
        for _ in range(self.top):
            layout.append(' ' * self.width)
        # Content area
        for line in content_lines:
            layout.append(' ' * self.left + line + ' ' * self.right)
        # Bottom margin
        for _ in range(self.bottom):
            layout.append(' ' * self.width)

        # Ensure total lines == self.height
        if len(layout) < self.height:
            layout += [' ' * self.width] * (self.height - len(layout))
        elif len(layout) > self.height:
            layout = layout[:self.height]

        return layout
