
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

        # Calculate the maximum height of each section
        section_heights = [len(section) for section in content_sections]

        # Check if the total height of all sections exceeds the available height
        total_height = sum(section_heights)
        if total_height > available_height:
            raise ValueError(
                "Total height of content sections exceeds available screen height")

        # Initialize the screen layout with empty lines
        screen_layout = [' ' * self.width for _ in range(self.height)]

        # Place the content sections on the screen
        y = self.top_margin
        for section in content_sections:
            section_height = len(section)
            for i, line in enumerate(section):
                # Trim or pad the line to fit the available width
                line = line[:available_width].ljust(available_width)
                screen_layout[y + i] = ' ' * self.left_margin + \
                    line + ' ' * self.right_margin
            y += section_height

        return screen_layout
