
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
        '''Create a full screen layout with the given content sections.
        Args:
            content_sections: A sequence of sequences of strings, where each inner sequence represents a section of content.
        Returns:
            A list of strings representing the full screen layout.
        '''
        available_width = self.width - self.left_margin - self.right_margin
        available_height = self.height - self.top_margin - self.bottom_margin

        # Calculate the height of each section
        section_heights = self._calculate_section_heights(
            content_sections, available_height)

        # Create the full screen layout
        layout = []
        # Add top margin
        layout.extend([' ' * self.width for _ in range(self.top_margin)])

        # Add content sections
        y = self.top_margin
        for i, section in enumerate(content_sections):
            section_height = section_heights[i]
            for line in section:
                if y >= self.height - self.bottom_margin:
                    break
                # Trim or pad the line to fit the available width
                formatted_line = line.ljust(available_width)[:available_width]
                layout.append(' ' * self.left_margin +
                              formatted_line + ' ' * self.right_margin)
                y += 1
            # Add empty lines to fill the section height
            for _ in range(section_height - len(section)):
                if y >= self.height - self.bottom_margin:
                    break
                layout.append(' ' * self.width)
                y += 1

        # Add bottom margin
        layout.extend([' ' * self.width for _ in range(self.height - y)])

        return layout

    def _calculate_section_heights(self, content_sections: Sequence[Sequence[str]], available_height: int) -> list[int]:
        '''Calculate the height of each section based on the available height.
        Args:
            content_sections: A sequence of sequences of strings, where each inner sequence represents a section of content.
            available_height: The available height for the content sections.
        Returns:
            A list of integers representing the height of each section.
        '''
        total_content_height = sum(len(section)
                                   for section in content_sections)
        if total_content_height == 0:
            return [0] * len(content_sections)

        # Calculate the height of each section proportionally
        section_heights = [int(len(section) / total_content_height *
                               available_height) for section in content_sections]

        # Adjust the section heights to add up to the available height
        remaining_height = available_height - sum(section_heights)
        for i in range(remaining_height):
            section_heights[i % len(section_heights)] += 1

        return section_heights
