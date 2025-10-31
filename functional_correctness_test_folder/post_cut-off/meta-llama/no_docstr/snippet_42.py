
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
        if not self.width or not self.height:
            raise ValueError("Screen dimensions are not set")

        available_width = self.width - \
            self.margins['left'] - self.margins['right']
        available_height = self.height - \
            self.margins['top'] - self.margins['bottom']

        if not available_width or not available_height:
            raise ValueError("Available screen space is zero")

        num_sections = len(content_sections)
        section_height = available_height // num_sections

        layout = []
        for i, section in enumerate(content_sections):
            section_layout = []
            y = self.margins['top'] + i * section_height
            for line in section:
                x = self.margins['left']
                section_layout.append(
                    ' ' * x + line + ' ' * (available_width - len(line)))
                y += 1
            layout.extend(section_layout +
                          [' ' * self.width] * (section_height - len(section)))

        # Handle the remaining height if available_height is not perfectly divisible by num_sections
        remaining_height = available_height % num_sections
        if remaining_height:
            start_index = len(layout)
            for i in range(remaining_height):
                layout.insert(start_index + i *
                              available_width, ' ' * self.width)

        # Adjust the layout to fit the available width
        adjusted_layout = []
        for line in layout:
            adjusted_layout.append(line.ljust(available_width).rjust(
                self.width - self.margins['right']))

        return adjusted_layout
