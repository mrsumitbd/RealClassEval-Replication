
from typing import Sequence


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
        '''Create a full screen layout with margins and content sections.
        Each section is a sequence of strings (lines). Lines are truncated or padded
        to fit the available width. The final layout is a list of strings, one per
        screen line, including top and bottom margins.
        '''
        # Calculate available width and height after margins
        avail_width = self.width - self.left - self.right
        avail_height = self.height - self.top - self.bottom

        if avail_width < 0 or avail_height < 0:
            raise ValueError("Margins exceed screen dimensions")

        layout: list[str] = []

        # Add top margin lines
        for _ in range(self.top):
            layout.append(' ' * self.width)

        # Add content sections
        for section in content_sections:
            for line in section:
                # Truncate or pad the line to the available width
                if len(line) > avail_width:
                    trimmed = line[:avail_width]
                else:
                    trimmed = line.ljust(avail_width)
                # Add left and right margins
                full_line = ' ' * self.left + trimmed + ' ' * self.right
                layout.append(full_line)

        # Add bottom margin lines
        for _ in range(self.bottom):
            layout.append(' ' * self.width)

        # Ensure the layout fits the screen height
        if len(layout) > self.height:
            # Truncate excess lines
            layout = layout[:self.height]
        else:
            # Pad with empty lines if necessary
            while len(layout) < self.height:
                layout.append(' ' * self.width)

        return layout
