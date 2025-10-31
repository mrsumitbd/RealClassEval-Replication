from typing import Sequence


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 80
        self.height = 24
        self._margin_left = 0
        self._margin_right = 0
        self._margin_top = 0
        self._margin_bottom = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError('width and height must be integers')
        if width < 0 or height < 0:
            raise ValueError('width and height must be non-negative')
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
        for name, val in [('left', left), ('right', right), ('top', top), ('bottom', bottom)]:
            if not isinstance(val, int):
                raise TypeError(f'margin {name} must be int')
            if val < 0:
                raise ValueError(f'margin {name} must be non-negative')
        self._margin_left = left
        self._margin_right = right
        self._margin_top = top
        self._margin_bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        content_sections = content_sections or []

        w = max(0, self.width)
        h = max(0, self.height)

        left_used = min(max(0, self._margin_left), w)
        right_used = min(max(0, self._margin_right), max(0, w - left_used))
        inner_width = max(0, w - left_used - right_used)

        top_used = min(max(0, self._margin_top), h)
        bottom_used = min(max(0, self._margin_bottom), max(0, h - top_used))
        content_capacity = max(0, h - top_used - bottom_used)

        lines: list[str] = []

        blank_full = ' ' * w
        blank_content_line = (' ' * left_used) + \
            (' ' * inner_width) + (' ' * right_used)

        for _ in range(top_used):
            lines.append(blank_full)

        produced = 0
        for section in content_sections:
            if produced >= content_capacity:
                break
            for raw_line in section:
                if produced >= content_capacity:
                    break
                line = '' if raw_line is None else str(raw_line).rstrip('\n')
                if inner_width > 0:
                    content = line[:inner_width].ljust(inner_width)
                else:
                    content = ''
                full_line = (' ' * left_used) + content + (' ' * right_used)
                # Ensure the line length is exactly screen width
                if len(full_line) < w:
                    full_line = full_line + (' ' * (w - len(full_line)))
                elif len(full_line) > w:
                    full_line = full_line[:w]
                lines.append(full_line)
                produced += 1

        while produced < content_capacity:
            lines.append(blank_content_line)
            produced += 1

        for _ in range(bottom_used):
            lines.append(blank_full)

        # Ensure final height
        if len(lines) < h:
            lines.extend([blank_full] * (h - len(lines)))
        elif len(lines) > h:
            lines = lines[:h]

        return lines
