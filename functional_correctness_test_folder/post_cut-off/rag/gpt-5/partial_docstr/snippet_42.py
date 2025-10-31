from typing import Sequence, Optional


class ScreenManager:
    """Manager for overall screen layout and organization."""

    def __init__(self) -> None:
        """Initialize screen manager."""
        self._width: Optional[int] = None
        self._height: Optional[int] = None
        self._margin_left: int = 0
        self._margin_right: int = 0
        self._margin_top: int = 0
        self._margin_bottom: int = 0
        self._section_separator: int = 1

    def set_screen_dimensions(self, width: int, height: int) -> None:
        """Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers")
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")
        self._width = width
        self._height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        """Set screen margins.
        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        """
        for name, val in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
            if not isinstance(val, int):
                raise TypeError(f"{name} margin must be integer")
            if val < 0:
                raise ValueError(f"{name} margin must be non-negative")
        self._margin_left = left
        self._margin_right = right
        self._margin_top = top
        self._margin_bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        """Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        """
        if self._width is None or self._height is None:
            raise RuntimeError(
                "Screen dimensions must be set before creating layout.")
        inner_width = self._width - (self._margin_left + self._margin_right)
        inner_height = self._height - (self._margin_top + self._margin_bottom)
        if inner_width <= 0 or inner_height <= 0:
            raise ValueError(
                "Screen dimensions too small for specified margins.")

        inner_blank = " " * inner_width
        inner_canvas: list[str] = [inner_blank for _ in range(inner_height)]

        row = 0
        last_section_index = len(content_sections) - 1
        for idx, section in enumerate(content_sections):
            if row >= inner_height:
                break
            for line in section:
                if row >= inner_height:
                    break
                truncated = (line[:inner_width]) if len(
                    line) > inner_width else line
                padded = truncated + (" " * (inner_width - len(truncated)))
                inner_canvas[row] = padded
                row += 1
            if idx != last_section_index and row < inner_height:
                sep_lines = min(self._section_separator, inner_height - row)
                for _ in range(sep_lines):
                    inner_canvas[row] = inner_blank
                    row += 1

        left_pad = " " * self._margin_left
        right_pad = " " * self._margin_right
        full_blank = " " * self._width

        output: list[str] = []
        output.extend(full_blank for _ in range(self._margin_top))
        for line in inner_canvas:
            output.append(f"{left_pad}{line}{right_pad}")
        output.extend(full_blank for _ in range(self._margin_bottom))

        # Ensure exact screen height (safety in case of miscalculation)
        if len(output) < self._height:
            output.extend(full_blank for _ in range(
                self._height - len(output)))
        elif len(output) > self._height:
            output = output[:self._height]

        return output
