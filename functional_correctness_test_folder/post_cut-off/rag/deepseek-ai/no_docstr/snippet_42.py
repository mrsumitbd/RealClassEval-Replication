
from typing import Sequence


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
        usable_width = self.width - self.left_margin - self.right_margin
        usable_height = self.height - self.top_margin - self.bottom_margin

        # Process each section to fit within margins
        processed_sections = []
        for section in content_sections:
            processed_section = []
            for line in section:
                # Truncate or pad each line to fit usable width
                processed_line = line[:usable_width].ljust(usable_width)
                processed_section.append(processed_line)
            processed_sections.append(processed_section)

        # Combine sections with appropriate spacing
        full_layout = []

        # Add top margin
        full_layout.extend(['' for _ in range(self.top_margin)])

        # Add content sections with spacing
        for i, section in enumerate(processed_sections):
            # Add section lines
            full_layout.extend(section)

            # Add spacing between sections (except after last section)
            if i < len(processed_sections) - 1:
                full_layout.append('')

        # Pad with empty lines if needed to reach full height
        while len(full_layout) < self.height - self.bottom_margin:
            full_layout.append('')

        # Add bottom margin
        full_layout.extend(['' for _ in range(self.bottom_margin)])

        # Apply left/right margins to each line
        final_layout = []
        for line in full_layout:
            margin_line = (' ' * self.left_margin) + \
                line + (' ' * self.right_margin)
            final_layout.append(margin_line)

        return final_layout
