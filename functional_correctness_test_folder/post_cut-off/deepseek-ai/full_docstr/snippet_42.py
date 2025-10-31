
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
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        layout = []
        content_width = self.width - self.left_margin - self.right_margin

        # Add top margin
        for _ in range(self.top_margin):
            layout.append(' ' * self.width)

        for section in content_sections:
            for line in section:
                # Apply left and right margins
                padded_line = (' ' * self.left_margin) + \
                    line.ljust(content_width) + (' ' * self.right_margin)
                # Ensure line doesn't exceed screen width
                layout.append(padded_line[:self.width])

        # Add bottom margin
        remaining_height = self.height - len(layout)
        for _ in range(remaining_height):
            layout.append(' ' * self.width)

        # Ensure total height doesn't exceed screen height
        return layout[:self.height]
