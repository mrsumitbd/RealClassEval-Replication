
from typing import Sequence, List


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

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> List[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        available_height = self.height - self.top_margin - self.bottom_margin
        available_width = self.width - self.left_margin - self.right_margin

        # Calculate the number of sections and their heights
        num_sections = len(content_sections)
        section_heights = [available_height // num_sections] * num_sections
        remainder = available_height % num_sections
        for i in range(remainder):
            section_heights[i] += 1

        layout = [' ' * self.width] * self.height

        current_line = self.top_margin
        for section, height in zip(content_sections, section_heights):
            for line in section[:height]:
                padded_line = line.ljust(available_width)
                layout[current_line + self.top_margin] = ' ' * \
                    self.left_margin + padded_line + ' ' * self.right_margin
                current_line += 1
            # Fill remaining lines in this section with spaces
            for _ in range(height - len(section)):
                layout[current_line + self.top_margin] = ' ' * self.width
                current_line += 1

        return layout
