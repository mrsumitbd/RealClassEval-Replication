
from __future__ import annotations
from typing import Sequence, List


class ScreenManager:
    def __init__(self) -> None:
        self._width: int | None = None
        self._height: int | None = None
        self._left_margin: int = 0
        self._right_margin: int = 0
        self._top_margin: int = 0
        self._bottom_margin: int = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Screen dimensions must be positive integers.")
        self._width = width
        self._height = height

    def set_margins(
        self,
        left: int = 0,
        right: int = 0,
        top: int = 0,
        bottom: int = 0,
    ) -> None:
        for name, value in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
            if value < 0:
                raise ValueError(f"{name} margin must be non‑negative.")
        self._left_margin = left
        self._right_margin = right
        self._top_margin = top
        self._bottom_margin = bottom

    def create_full_screen_layout(
        self, content_sections: Sequence[Sequence[str]]
    ) -> List[str]:
        if self._width is None or self._height is None:
            raise RuntimeError(
                "Screen dimensions must be set before creating layout.")

        width = self._width
        height = self._height
        left = self._left_margin
        right = self._right_margin
        top = self._top_margin
        bottom = self._bottom_margin

        usable_width = max(0, width - left - right)
        usable_height = max(0, height - top - bottom)

        # Prepare the full screen buffer
        screen: List[str] = []

        # Top margin
        for _ in range(top):
            screen.append(" " * width)

        # Content area
        # Flatten content sections into a single list of lines
        content_lines: List[str] = []
        for section in content_sections:
            content_lines.extend(section)

        # Iterate over usable height lines
        for i in range(usable_height):
            if i < len(content_lines):
                raw_line = content_lines[i]
                # Truncate or pad the line to usable width
                line = raw_line[:usable_width].ljust(usable_width)
            else:
                line = " " * usable_width
            # Add left and right margins
            full_line = " " * left + line + " " * right
            screen.append(full_line)

        # Bottom margin
        for _ in range(bottom):
            screen.append(" " * width)

        # If the screen buffer is shorter than the requested height (due to negative margins),
        # pad with empty lines at the bottom
        while len(screen) < height:
            screen.append(" " * width)

        # If the screen buffer is longer than the requested height, truncate it
        if len(screen) > height:
            screen = screen[:height]

        return screen
