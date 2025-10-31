
from typing import Sequence


class ScreenManager:

    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        layout = []
        content_width = self.width - self.left_margin - self.right_margin
        content_height = self.height - self.top_margin - self.bottom_margin

        for section in content_sections:
            section_layout = []
            for line in section:
                if len(line) > content_width:
                    line = line[:content_width]
                padded_line = line.ljust(content_width)
                section_layout.append(padded_line)

            while len(section_layout) < content_height:
                section_layout.append(' ' * content_width)

            layout.extend(section_layout[:content_height])

        return layout
