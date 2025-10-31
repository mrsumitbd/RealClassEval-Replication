
from typing import Sequence


class ScreenManager:

    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def set_screen_dimensions(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        usable_width = self.width - self.left - self.right
        usable_height = self.height - self.top - self.bottom

        # Flatten content_sections into lines, then pad/truncate each line to usable_width
        content_lines = []
        for section in content_sections:
            for line in section:
                if len(line) < usable_width:
                    line = line + ' ' * (usable_width - len(line))
                else:
                    line = line[:usable_width]
                content_lines.append(line)
        # Pad or truncate content_lines to usable_height
        if len(content_lines) < usable_height:
            content_lines += [' ' * usable_width] * \
                (usable_height - len(content_lines))
        else:
            content_lines = content_lines[:usable_height]

        # Add top and bottom margins
        top_margin = [' ' * self.width] * self.top
        bottom_margin = [' ' * self.width] * self.bottom

        # Add left and right margins to each content line
        final_lines = []
        for line in content_lines:
            final_line = (' ' * self.left) + line + (' ' * self.right)
            final_lines.append(final_line)

        return top_margin + final_lines + bottom_margin
