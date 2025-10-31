
from __future__ import annotations
from typing import Sequence, List


class ScreenManager:
    """Manager for overall screen layout and organization."""

    def __init__(self) -> None:
        """Initialize screen manager."""
        # Default terminal size (common defaults)
        self.width: int = 80
        self.height: int = 24
        # Margins in characters/lines
        self.left: int = 0
        self.right: int = 0
        self.top: int = 0
        self.bottom: int = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        """Set screen dimensions for layout calculations.

        Args:
            width: Screen width in characters
            height: Screen height in lines
        """
        if width <= 0 or height <= 0:
            raise ValueError(
                "Screen width and height must be positive integers.")
        self.width = width
        self.height = height

    def set_margins(
        self,
        left: int = 0,
        right: int = 0,
        top: int = 0,
        bottom: int = 0,
    ) -> None:
        """Set screen margins.

        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        """
        for name, value in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
            if value < 0:
                raise ValueError(f"{name} margin must be non‑negative.")
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def create_full_screen_layout(
        self, content_sections: Sequence[Sequence[str]]
    ) -> List[str]:
        """Create full screen layout with multiple content sections.

        Args:
            content_sections: List of content sections, each being a list of lines

        Returns:
            Combined screen layout as list of lines
        """
        # Compute usable area
        inner_width = max(0, self.width - self.left - self.right)
        inner_height = max(0, self.height - self.top - self.bottom)

        # Helper to create a blank line of full width
        blank_line = " " * self.width

        # Start with top margin
        layout: List[str] = [blank_line] * self.top

        # Add content
        for section in content_sections:
            for raw_line in section:
                # Truncate or pad to inner width
                line = raw_line[:inner_width].ljust(inner_width)
                # Add left/right margins
                full_line = " " * self
