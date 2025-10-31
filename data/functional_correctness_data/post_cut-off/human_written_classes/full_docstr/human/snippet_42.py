from typing import Final, Sequence

class ScreenManager:
    """Manager for overall screen layout and organization."""
    DEFAULT_SCREEN_WIDTH: Final[int] = 80
    DEFAULT_SCREEN_HEIGHT: Final[int] = 24
    DEFAULT_MARGIN: Final[int] = 0

    def __init__(self) -> None:
        """Initialize screen manager."""
        self.screen_width: int = self.DEFAULT_SCREEN_WIDTH
        self.screen_height: int = self.DEFAULT_SCREEN_HEIGHT
        self.margin_left: int = self.DEFAULT_MARGIN
        self.margin_right: int = self.DEFAULT_MARGIN
        self.margin_top: int = self.DEFAULT_MARGIN
        self.margin_bottom: int = self.DEFAULT_MARGIN

    def set_screen_dimensions(self, width: int, height: int) -> None:
        """Set screen dimensions for layout calculations.

        Args:
            width: Screen width in characters
            height: Screen height in lines
        """
        self.screen_width = width
        self.screen_height = height

    def set_margins(self, left: int=0, right: int=0, top: int=0, bottom: int=0) -> None:
        """Set screen margins.

        Args:
            left: Left margin in characters
            right: Right margin in characters
            top: Top margin in lines
            bottom: Bottom margin in lines
        """
        self.margin_left = left
        self.margin_right = right
        self.margin_top = top
        self.margin_bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        """Create full screen layout with multiple content sections.

        Args:
            content_sections: List of content sections, each being a list of lines

        Returns:
            Combined screen layout as list of lines
        """
        screen_buffer: list[str] = []
        screen_buffer.extend([''] * self.margin_top)
        for i, section in enumerate(content_sections):
            if i > 0:
                screen_buffer.append('')
            for line in section:
                padded_line: str = ' ' * self.margin_left + line
                screen_buffer.append(padded_line)
        screen_buffer.extend([''] * self.margin_bottom)
        return screen_buffer