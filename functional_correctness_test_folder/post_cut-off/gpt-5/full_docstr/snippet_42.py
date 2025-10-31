from typing import Sequence, List


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self._width: int | None = None
        self._height: int | None = None
        self._margin_left: int = 0
        self._margin_right: int = 0
        self._margin_top: int = 0
        self._margin_bottom: int = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers")
        if width < 0 or height < 0:
            raise ValueError("width and height must be non-negative")
        self._width = width
        self._height = height
        if self._width is not None and self._height is not None:
            if self._margin_left + self._margin_right > self._width:
                raise ValueError(
                    "Sum of left and right margins exceeds screen width")
            if self._margin_top + self._margin_bottom > self._height:
                raise ValueError(
                    "Sum of top and bottom margins exceeds screen height")

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        '''Set screen margins.
        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        '''
        for name, val in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
            if not isinstance(val, int):
                raise TypeError(f"{name} margin must be an integer")
            if val < 0:
                raise ValueError(f"{name} margin must be non-negative")
        self._margin_left = left
        self._margin_right = right
        self._margin_top = top
        self._margin_bottom = bottom
        if self._width is not None and self._height is not None:
            if self._margin_left + self._margin_right > self._width:
                raise ValueError(
                    "Sum of left and right margins exceeds screen width")
            if self._margin_top + self._margin_bottom > self._height:
                raise ValueError(
                    "Sum of top and bottom margins exceeds screen height")

    def _content_dims(self) -> tuple[int, int]:
        if self._width is None or self._height is None:
            raise ValueError("Screen dimensions not set")
        content_width = self._width - (self._margin_left + self._margin_right)
        content_height = self._height - \
            (self._margin_top + self._margin_bottom)
        return content_width, content_height

    def _wrap_line(self, line: str, width: int) -> List[str]:
        if width <= 0:
            return []
        if not line:
            return [""]
        # Hard wrap by fixed width chunks
        return [line[i:i+width] for i in range(0, len(line), width)]

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        content_width, content_height = self._content_dims()
        if self._width is None or self._height is None:
            raise ValueError("Screen dimensions not set")
        if content_width <= 0 or content_height <= 0:
            return []

        content_lines: List[str] = []
        first_section = True
        for section in content_sections or []:
            if not first_section:
                content_lines.append("")  # separator line between sections
            first_section = False
            for line in section:
                wrapped = self._wrap_line(str(line), content_width)
                if not wrapped:
                    # when width <= 0 would have early returned, but safeguard
                    continue
                content_lines.extend(wrapped)

        # Trim or pad to fit content height
        if len(content_lines) > content_height:
            content_lines = content_lines[:content_height]
        else:
            content_lines.extend([""] * (content_height - len(content_lines)))

        # Compose full lines with margins
        left_pad = " " * self._margin_left
        right_pad = " " * self._margin_right
        full_lines: List[str] = []

        # Top margin
        full_lines.extend([(" " * self._width)] * self._margin_top)

        # Content area
        for line in content_lines:
            # Ensure line fits content width
            if len(line) < content_width:
                line = line + (" " * (content_width - len(line)))
            elif len(line) > content_width:
                line = line[:content_width]
            full_lines.append(f"{left_pad}{line}{right_pad}")

        # Bottom margin
        full_lines.extend([(" " * self._width)] * self._margin_bottom)

        # Ensure final height matches screen height (in case of zero height)
        if len(full_lines) != self._height:
            if self._height == 0:
                return []
            # Adjust by trimming or padding empty lines
            if len(full_lines) > self._height:
                full_lines = full_lines[:self._height]
            else:
                full_lines.extend([(" " * self._width)] *
                                  (self._height - len(full_lines)))

        return full_lines
