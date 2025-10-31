
from typing import Sequence


class ScreenManager:
    """Manager for overall screen layout and organization."""

    def __init__(self) -> None:
        """Initialize screen manager."""
        self.width = 0
        self.height = 0
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        """Set screen dimensions for layout calculations.

        Args:
            width: Screen width in characters
            height: Screen height in lines
        """
        self.width = width
        self.height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        """Set screen margins.

        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        """
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        """Create full screen layout with multiple content sections.

        Args:
            content_sections: List of content sections, each being a list of lines

        Returns:
            Combined screen layout as list of lines
        """
        available_width = self.width - self.left_margin - self.right_margin
        available_height = self.height - self.top_margin - self.bottom_margin

        # Calculate the height of each section
        section_heights = [len(section) for section in content_sections]
        total_section_height = sum(section_heights)

        # If total height exceeds available height, truncate sections
        if total_section_height > available_height:
            ratio = available_height / total_section_height
            section_heights = [int(height * ratio)
                               for height in section_heights]
            # Adjust the last section to fill any remaining space
            section_heights[-1] += available_height - sum(section_heights)

        screen_layout = []
        # Add top margin
        screen_layout.extend(
            [' ' * self.width for _ in range(self.top_margin)])

        y = self.top_margin
        for i, section in enumerate(content_sections):
            section_height = section_heights[i]
            section = section[:section_height]  # Truncate section if necessary
            # Add left margin and section content
            for line in section:
                padded_line = ' ' * self.left_margin + \
                    line.ljust(available_width) + ' ' * self.right_margin
                screen_layout.append(padded_line)
                y += 1
            # Add empty lines to fill the remaining height of the section
            while y < self.top_margin + sum(section_heights[:i+1]):
                screen_layout.append(' ' * self.width)
                y += 1

        # Add bottom margin
        screen_layout.extend(
            [' ' * self.width for _ in range(self.height - y)])

        return screen_layout
