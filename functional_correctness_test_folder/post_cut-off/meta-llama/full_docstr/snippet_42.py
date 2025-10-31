
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
        available_width = self.width - self.left_margin - self.right_margin
        available_height = self.height - self.top_margin - self.bottom_margin

        # Calculate the height of each section
        total_content_height = sum(len(section)
                                   for section in content_sections)
        if total_content_height > available_height:
            raise ValueError("Total content height exceeds available height")

        # Create the layout
        layout = []
        # Add top margin
        layout.extend([' ' * self.width for _ in range(self.top_margin)])

        # Add content sections
        for section in content_sections:
            for line in section:
                # Truncate or pad the line to fit the available width
                formatted_line = (
                    line[:available_width] + ' ' * available_width)[:available_width]
                layout.append(' ' * self.left_margin +
                              formatted_line + ' ' * self.right_margin)
            # Add empty lines to separate sections if there's remaining space
            remaining_height = available_height - \
                len(layout) + self.top_margin + \
                self.bottom_margin - len(layout)
            if remaining_height > 0:
                layout.extend(
                    [' ' * self.width for _ in range(min(remaining_height, available_height - len(section)))])

        # Adjust the layout to fit the available height
        while len(layout) < self.height:
            layout.append(' ' * self.width)

        # Ensure the layout doesn't exceed the available height
        layout = layout[:self.height]

        return layout
