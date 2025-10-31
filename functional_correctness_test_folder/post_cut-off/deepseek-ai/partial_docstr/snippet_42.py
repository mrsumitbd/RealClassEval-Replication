
from typing import Sequence


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 0
        self.height = 0
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

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
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create a full screen layout with margins and content sections.
        Args:
            content_sections: A sequence of content sections, each being a sequence of strings.
        Returns:
            A list of strings representing the full screen layout.
        '''
        layout = []
        content_width = self.width - self.left_margin - self.right_margin
        content_height = self.height - self.top_margin - self.bottom_margin

        if content_width <= 0 or content_height <= 0:
            return []

        empty_line = ' ' * self.width

        for _ in range(self.top_margin):
            layout.append(empty_line)

        for section in content_sections:
            for line in section:
                if len(line) > content_width:
                    line = line[:content_width]
                padded_line = (' ' * self.left_margin) + \
                    line.ljust(content_width) + (' ' * self.right_margin)
                layout.append(padded_line)

        remaining_lines = content_height - len(layout) + self.top_margin
        for _ in range(remaining_lines):
            layout.append(empty_line)

        for _ in range(self.bottom_margin):
            layout.append(empty_line)

        return layout
