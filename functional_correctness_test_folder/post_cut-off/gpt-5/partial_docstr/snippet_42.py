from typing import Sequence, List


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self._width: int = 0
        self._height: int = 0
        self._left: int = 0
        self._right: int = 0
        self._top: int = 0
        self._bottom: int = 0

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
                raise TypeError(f"{name} must be an integer")
            if val < 0:
                raise ValueError(f"{name} must be non-negative")
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> List[str]:
        width = self._width
        height = self._height

        if width <= 0 or height <= 0:
            return []

        screen_rows: List[List[str]] = [
            list(' ' * width) for _ in range(height)]

        content_width = width - self._left - self._right
        content_height = height - self._top - self._bottom

        if content_width <= 0 or content_height <= 0:
            return [''.join(row) for row in screen_rows]

        flat_lines: List[str] = []
        remaining = content_height

        for section in content_sections:
            for line in section:
                if remaining <= 0:
                    break
                # Handle embedded newlines gracefully
                for part in str(line).splitlines() or [""]:
                    if remaining <= 0:
                        break
                    text = part
                    if text == "":
                        flat_lines.append("")
                        remaining -= 1
                        continue
                    start = 0
                    tlen = len(text)
                    while start < tlen and remaining > 0:
                        slice_part = text[start:start + content_width]
                        flat_lines.append(slice_part)
                        remaining -= 1
                        start += content_width
            if remaining <= 0:
                break

        y = self._top
        x_start = self._left
        x_end = x_start + content_width

        for line in flat_lines:
            if y >= self._top + content_height or y >= height:
                break
            content = (line[:content_width]).ljust(content_width)
            screen_rows[y][x_start:x_end] = list(content)
            y += 1

        return [''.join(row) for row in screen_rows]
