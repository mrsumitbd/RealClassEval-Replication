
class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 0
        self.height = 0
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

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
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        '''Create full screen layout with multiple content sections.
        Args:
            content_sections: List of content sections, each being a list of lines
        Returns:
            Combined screen layout as list of lines
        '''
        if not self.width or not self.height:
            raise ValueError(
                "Screen dimensions not set. Call set_screen_dimensions first.")

        # Calculate available width and height after margins
        available_width = self.width - self.left_margin - self.right_margin
        available_height = self.height - self.top_margin - self.bottom_margin

        # Initialize screen layout with empty lines
        screen_layout = [' ' * self.width for _ in range(self.height)]

        # Add top margin
        for i in range(self.top_margin):
            screen_layout[i] = ' ' * self.width

        # Add bottom margin
        for i in range(self.height - self.bottom_margin, self.height):
            screen_layout[i] = ' ' * self.width

        # Calculate section heights (distribute available height equally)
        section_height = available_height // len(content_sections)
        remaining_height = available_height % len(content_sections)

        # Add content sections
        current_line = self.top_margin
        for i, section in enumerate(content_sections):
            # Determine section height (distribute remaining lines)
            lines_to_use = section_height + (1 if i < remaining_height else 0)

            # Add left margin
            for j in range(lines_to_use):
                if current_line + j < self.height - self.bottom_margin:
                    screen_layout[current_line + j] = (' ' * self.left_margin) + \
                        (section[j] if j < len(section) else '').ljust(available_width) + \
                        (' ' * self.right_margin)

            current_line += lines_to_use

        return screen_layout
