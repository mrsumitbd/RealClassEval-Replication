
from __future__ import annotations

from typing import Sequence, List


class ScreenManager:
    """Manager for overall screen layout and organization."""

    def __init__(self) -> None:
        """Initialize screen manager with default dimensions and margins."""
        self.width: int = 80
        self.height: int = 24
        self.left_margin: int = 0
        self.right_margin: int = 0
        self.top_margin: int = 0
        self.bottom_margin: int = 0

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
        for name, value in (
            ("left", left),
            ("right", right),
            ("top", top),
            ("bottom", bottom),
        ):
            if value < 0:
                raise ValueError(f"{name} margin must be non‑negative.")
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def create_full_screen_layout(
        self, content_sections: Sequence[Sequence[str]]
    ) -> List[str]:
        """Create full screen layout with multiple content sections.

        Args:
            content_sections: List of content sections, each being a list of lines

        Returns:
            Combined screen layout as list of lines
        """
        # Compute usable width and height
        usable_width = self.width - self.left_margin - self.right_margin
        if usable_width <= 0:
            raise ValueError("Margins exceed screen width.")
        usable_height = self.height - self.top_margin - self.bottom_margin
        if usable_height <= 0:
            raise ValueError("Margins exceed screen height.")

        # Helper to format a single line
        def format_line(line: str) -> str:
            # Truncate or pad to usable width
            if len(line) > usable_width:
                line = line[:usable_width]
            else:
                line = line.ljust(usable_width)
            # Add left and right margins
            return (" " * self.left_margin) + line + (" " * self.right_margin)

        # Build content lines
        content_lines: List[str] = []
        for section in content_sections:
            for raw_line in section:
                content_lines.append(format_line(raw_line))
            # Add a blank line between sections (optional)
            content_lines.append(format_line(""))

        # Trim or pad to usable height
        if len(content_lines) > usable_height:
            # Truncate excess lines
            content_lines = content_lines[:usable_height]
        else:
            # Pad with empty lines
            empty_line = format_line("")
            while len(content_lines) < usable_height:
                content_lines.append(empty_line)

        # Add top and bottom margins
        top_margin_lines = [" " * self.width] * self.top_margin
        bottom_margin_lines = [" " * self.width] * self.bottom_margin

        full_layout = top_margin_lines + content_lines + bottom_margin_lines

        # Ensure final layout matches requested height
        if len(full_layout) > self.height:
            full_layout = full_layout[: self.height]
        elif len(full_layout) < self.height:
            # Pad with empty lines at the bottom if needed
            empty_line = " " * self.width
            while len(full_layout) < self.height:
                full_layout.append(empty_line)

        return full_layout
