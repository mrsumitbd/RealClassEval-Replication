
from typing import Dict, Any, Literal


class Text_background:

    def __init__(
        self,
        *,
        color: str,
        style: Literal[1, 2] = 1,
        alpha: float = 1.0,
        round_radius: float = 0.0,
        height: float = 0.14,
        width: float = 0.14,
        horizontal_offset: float = 0.5,
        vertical_offset: float = 0.5
    ):
        self.color = color
        self.style = style
        self.alpha = alpha
        self.round_radius = round_radius
        self.height = height
        self.width = width
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

    def export_json(self) -> Dict[str, Any]:
        return {
            "color": self.color,
            "style": self.style,
            "alpha": self.alpha,
            "round_radius": self.round_radius,
            "height": self.height,
            "width": self.width,
            "horizontal_offset": self.horizontal_offset,
            "vertical_offset": self.vertical_offset
        }
