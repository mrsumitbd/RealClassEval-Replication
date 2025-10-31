
from typing import Sequence


class ScreenManager:

    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.margins = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    def set_screen_dimensions(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        self.margins['left'] = left
        self.margins['right'] = right
        self.margins['top'] = top
        self.margins['bottom'] = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        layout = []
        content_height = self.height - \
            self.margins['top'] - self.margins['bottom']
        content_width = self.width - \
            self.margins['left'] - self.margins['right']

        for section in content_sections:
            formatted_section = []
            for line in section:
                formatted_section.append(line.ljust(content_width))
            layout.extend(formatted_section)

        return layout
