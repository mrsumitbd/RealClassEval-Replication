from typing import Sequence, Optional


class ScreenManager:

    def __init__(self) -> None:
        self._width: Optional[int] = None
        self._height: Optional[int] = None
        self._margins = {"left": 0, "right": 0, "top": 0, "bottom": 0}

    def set_screen_dimensions(self, width: int, height: int) -> None:
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers")
        if width < 0 or height < 0:
            raise ValueError("width and height must be non-negative")
        self._width = width
        self._height = height
        self._validate_dimensions_vs_margins()

    def set_margins(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0) -> None:
        for name, val in (("left", left), ("right", right), ("top", top), ("bottom", bottom)):
            if not isinstance(val, int):
                raise TypeError(f"{name} margin must be an integer")
            if val < 0:
                raise ValueError(f"{name} margin must be non-negative")
        self._margins["left"] = left
        self._margins["right"] = right
        self._margins["top"] = top
        self._margins["bottom"] = bottom
        self._validate_dimensions_vs_margins()

    def create_full_screen_layout(self, content_sections: Sequence[Sequence[str]]) -> list[str]:
        if self._width is None or self._height is None:
            raise RuntimeError(
                "Screen dimensions must be set before creating layout")
        inner_width = self._width - \
            (self._margins["left"] + self._margins["right"])
        inner_height = self._height - \
            (self._margins["top"] + self._margins["bottom"])
        if inner_width < 0 or inner_height < 0:
            raise ValueError("Margins exceed screen dimensions")

        top_pad = [" " * self._width] * self._margins["top"]
        bottom_pad = [" " * self._width] * self._margins["bottom"]
        left_spaces = " " * self._margins["left"]
        right_spaces = " " * self._margins["right"]

        content_lines: list[str] = []
        for section in content_sections:
            for line in section:
                if len(content_lines) >= inner_height:
                    break
                s = str(line)
                if inner_width > 0:
                    if len(s) > inner_width:
                        s = s[:inner_width]
                    else:
                        s = s + " " * (inner_width - len(s))
                else:
                    s = ""  # inner width is zero
                content_lines.append(f"{left_spaces}{s}{right_spaces}")
            if len(content_lines) >= inner_height:
                break

        while len(content_lines) < inner_height:
            content_lines.append(
                f"{left_spaces}{' ' * max(inner_width, 0)}{right_spaces}")

        return top_pad + content_lines + bottom_pad

    def _validate_dimensions_vs_margins(self) -> None:
        if self._width is None or self._height is None:
            return
        total_h_margin = self._margins["left"] + self._margins["right"]
        total_v_margin = self._margins["top"] + self._margins["bottom"]
        if total_h_margin > self._width or total_v_margin > self._height:
            raise ValueError("Sum of margins cannot exceed screen dimensions")
