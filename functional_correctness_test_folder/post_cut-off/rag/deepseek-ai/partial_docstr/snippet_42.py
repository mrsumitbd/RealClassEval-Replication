
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

        if usable_width <= 0 or usable_height <= 0:
            return []

        # Process each section to fit within margins
        processed_sections = []
        for section in content_sections:
            processed_section = []
            for line in section:
                # Apply left margin and truncate to usable width
                processed_line = (' ' * self.left_margin) + line[:usable_width]
                processed_section.append(processed_line)
            processed_sections.append(processed_section)

        # Combine sections with top and bottom margins
        full_layout = []

        # Top margin
        full_layout.extend([''] * self.top_margin)

        # Content sections
        remaining_height = usable_height
        for section in processed_sections:
            if remaining_height <= 0:
                break
            section_height = min(len(section), remaining_height)
            full_layout.extend(section[:section_height])
            remaining_height -= section_height

        # Fill remaining space if needed
        if remaining_height > 0:
            full_layout.extend([''] * remaining_height)

        # Bottom margin
        full_layout.extend([''] * self.bottom_margin)

        return full_layout
