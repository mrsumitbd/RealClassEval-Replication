
from __future__ import annotations

from typing import Any, Dict, Literal


class Text_background:
    """
    Represents a text background configuration for a video editing context.

    Attributes
    ----------
    color : str
        Background color in the format '#RRGGBB'.
    style : Literal[1, 2]
        Background style identifier (1 or 2).
    alpha : float
        Opacity of the background, range [0, 1].
    round_radius : float
        Corner radius of the background, range [0, 1].
    height : float
        Height of the background relative to the canvas, range [0, 1].
    width : float
        Width of the background relative to the canvas, range [0, 1].
    horizontal_offset : float
        Horizontal offset of the background relative to the canvas, range [0, 1].
    vertical_offset : float
        Vertical offset of the background relative to the canvas, range [0, 1].
    """

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
        vertical_offset: float = 0.5,
    ) -> None:
        # Validate color
        if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
            raise ValueError(
                f"color must be a string in the format '#RRGGBB', got {color!r}"
            )
        # Validate style
        if style not in (1, 2):
            raise ValueError(f"style must be 1 or 2, got {style!r}")
        # Validate numeric ranges
        for name, value in (
            ("alpha", alpha),
            ("round_radius", round_radius),
            ("height", height),
            ("width", width),
            ("horizontal_offset", horizontal_offset),
            ("vertical_offset", vertical_offset),
        ):
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"{name} must be a number, got {type(value).__name__}")
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1], got {value!r}")

        self.color = color.upper()
        self.style = style
        self.alpha = float(alpha)
        self.round_radius = float(round_radius)
        self.height = float(height)
        self.width = float(width)
        self.horizontal_offset = float(horizontal_offset)
        self.vertical_offset = float(vertical_offset)

    def export_json(self) -> Dict[str, Any]:
        """
        Generate a JSON-compatible dictionary representing the background.

        Returns
        -------
        dict
            Dictionary with keys matching the expected JSON schema.
        """
        return {
            "color": self.color,
            "style": self.style,
            "alpha": self.alpha,
            "roundRadius": self.round_radius,
            "height": self.height,
            "width": self.width,
            "horizontalOffset": self.horizontal_offset,
            "verticalOffset": self.vertical_offset,
        }
