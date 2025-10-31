from typing import Sequence


class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 80
        self.height = 24
        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        '''Set screen dimensions for layout calculations.
        Args:
            width: Screen width in characters
            height: Screen height in lines
        '''
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
        self.margin_left = left
        self.margin_right = right
        self.margin_top = top
        self.margin_bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        usable_width = self.width - self.margin_left - self.margin_right
        usable_height = self.height - self.margin_top - self.margin_bottom

        # Flatten all content sections into a single list of lines
        content_lines = []
        for section in content_sections:
            content_lines.extend(section)

        # Truncate or pad content_lines to fit usable_height
        if len(content_lines) > usable_height:
            content_lines = content_lines[:usable_height]
        else:
            content_lines += [''] * (usable_height - len(content_lines))

        # Pad each line to usable_width and add left/right margins
        padded_lines = []
        for line in content_lines:
            line = line[:usable_width]
            line = line.ljust(usable_width)
            full_line = ' ' * self.margin_left + line + ' ' * self.margin_right
            padded_lines.append(full_line)

        # Add top and bottom margins as blank lines
        top_margin_lines = [' ' * self.width] * self.margin_top
        bottom_margin_lines = [' ' * self.width] * self.margin_bottom

        return top_margin_lines + padded_lines + bottom_margin_lines
