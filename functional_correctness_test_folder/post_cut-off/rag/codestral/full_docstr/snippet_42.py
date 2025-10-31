
class ScreenManager:
    '''Manager for overall screen layout and organization.'''

    def __init__(self) -> None:
        '''Initialize screen manager.'''
        self.width = 80
        self.height = 24
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
        screen_layout = []
        available_width = self.width - self.left_margin - self.right_margin
        available_height = self.height - self.top_margin - self.bottom_margin

        # Add top margin
        screen_layout.extend([''] * self.top_margin)

        # Process each content section
        for section in content_sections:
            # Add left margin to each line in the section
            section_with_margins = [(' ' * self.left_margin) + line.ljust(
                available_width) + (' ' * self.right_margin) for line in section]
            screen_layout.extend(section_with_margins)

        # Add bottom margin
        screen_layout.extend([''] * self.bottom_margin)

        # Ensure the layout fits the screen dimensions
        if len(screen_layout) > self.height:
            screen_layout = screen_layout[:self.height]

        return screen_layout
