from typing import Sequence, List, Optional


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self._width: Optional[int] = None
        self._height: Optional[int] = None
        self._margin_left: int = 0
        self._margin_right: int = 0
        self._margin_top: int = 0
        self._margin_bottom: int = 0
        self._section_spacing: int = 1  # blank inner lines between sections

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError('width and height must be integers')
        if width <= 0 or height <= 0:
            raise ValueError('width and height must be positive')
        self._width = width
        self._height = height
        self._validate_inner_dimensions()

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        '''Set screen margins.
        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        '''
        for name, val in (('left', left), ('right', right), ('top', top), ('bottom', bottom)):
            if not isinstance(val, int):
                raise TypeError(f'{name} margin must be an integer')
            if val < 0:
                raise ValueError(f'{name} margin must be >= 0')
        self._margin_left = left
        self._margin_right = right
        self._margin_top = top
        self._margin_bottom = bottom
        self._validate_inner_dimensions()

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        self._ensure_dimensions_set()
        self._validate_inner_dimensions()

        inner_w = self._inner_width()
        inner_h = self._inner_height()
        if inner_w <= 0 or inner_h <= 0:
            # Should not happen due to validation, but keep safe.
            return [' ' * self._width for _ in range(self._height)]

        inner_lines: List[str] = []

        for idx, section in enumerate(content_sections or []):
            # Add a spacer between sections, but not before the first
            if idx > 0 and self._section_spacing > 0:
                inner_lines.extend([''] * self._section_spacing)

            # Add wrapped lines of this section
            for raw_line in section:
                line = raw_line.rstrip('\n')
                wrapped = self._wrap_to_width(line, inner_w)
                if not wrapped:
                    inner_lines.append('')
                else:
                    inner_lines.extend(wrapped)

        # Trim or pad inner content to fit inner height
        if len(inner_lines) > inner_h:
            inner_lines = inner_lines[:inner_h]
        else:
            inner_lines.extend([''] * (inner_h - len(inner_lines)))

        # Construct full lines with margins
        left_spaces = ' ' * self._margin_left
        right_spaces = ' ' * self._margin_right
        full_lines: List[str] = []

        # Top margin
        full_lines.extend([' ' * self._width for _ in range(self._margin_top)])

        # Content area
        for line in inner_lines:
            content = (line[:inner_w]).ljust(inner_w)
            full_line = f'{left_spaces}{content}{right_spaces}'
            # Ensure exact width
            full_lines.append(full_line[:self._width].ljust(self._width))

        # Bottom margin
        full_lines.extend(
            [' ' * self._width for _ in range(self._margin_bottom)])

        # Ensure final size exactly equals screen height
        if len(full_lines) > self._height:
            full_lines = full_lines[:self._height]
        elif len(full_lines) < self._height:
            full_lines.extend(
                [' ' * self._width for _ in range(self._height - len(full_lines))])

        return full_lines

    # Helpers

    def _ensure_dimensions_set(self) -> None:
        if self._width is None or self._height is None:
            raise RuntimeError(
                'Screen dimensions must be set before creating layout.')

    def _inner_width(self) -> int:
        if self._width is None:
            return 0
        return self._width - self._margin_left - self._margin_right

    def _inner_height(self) -> int:
        if self._height is None:
            return 0
        return self._height - self._margin_top - self._margin_bottom

    def _validate_inner_dimensions(self) -> None:
        if self._width is None or self._height is None:
            return
        if self._margin_left + self._margin_right > self._width:
            raise ValueError('Horizontal margins exceed screen width')
        if self._margin_top + self._margin_bottom > self._height:
            raise ValueError('Vertical margins exceed screen height')
        if self._inner_width() <= 0:
            raise ValueError('Inner width must be positive')
        if self._inner_height() <= 0:
            raise ValueError('Inner height must be positive')

    @staticmethod
    def _wrap_to_width(text: str, width: int) -> List[str]:
        if width <= 0:
            return []
        if text == '':
            return ['']
        lines: List[str] = []
        i = 0
        n = len(text)
        while i < n:
            lines.append(text[i:i + width])
            i += width
        return lines
