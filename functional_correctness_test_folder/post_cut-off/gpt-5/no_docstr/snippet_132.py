from typing import Any, Dict, Literal
import math


class Text_background:

    def __init__(self, *, color: str, style: Literal[1, 2] = 1, alpha: float = 1.0, round_radius: float = 0.0, height: float = 0.14, width: float = 0.14, horizontal_offset: float = 0.5, vertical_offset: float = 0.5):
        if not isinstance(color, str) or not color:
            raise ValueError("color must be a non-empty string")
        if style not in (1, 2):
            raise ValueError("style must be 1 or 2")
        self._alpha = self._validate_float("alpha", alpha, 0.0, 1.0)
        self._round_radius = self._validate_float(
            "round_radius", round_radius, 0.0, None)
        self._height = self._validate_float(
            "height", height, 0.0, None, strict_lower=True)
        self._width = self._validate_float(
            "width", width, 0.0, None, strict_lower=True)
        self._horizontal_offset = self._validate_float(
            "horizontal_offset", horizontal_offset, 0.0, 1.0)
        self._vertical_offset = self._validate_float(
            "vertical_offset", vertical_offset, 0.0, 1.0)

        self._color = color
        self._style = style

    @staticmethod
    def _validate_float(name: str, value: float, min_value: float | None, max_value: float | None, strict_lower: bool = False) -> float:
        if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
            raise ValueError(f"{name} must be a finite number")
        v = float(value)
        if min_value is not None:
            if strict_lower:
                if not (v > min_value):
                    raise ValueError(f"{name} must be > {min_value}")
            else:
                if not (v >= min_value):
                    raise ValueError(f"{name} must be >= {min_value}")
        if max_value is not None and not (v <= max_value):
            raise ValueError(f"{name} must be <= {max_value}")
        return v

    @property
    def color(self) -> str:
        return self._color

    @property
    def style(self) -> Literal[1, 2]:
        return self._style

    @property
    def alpha(self) -> float:
        return self._alpha

    @property
    def round_radius(self) -> float:
        return self._round_radius

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @property
    def horizontal_offset(self) -> float:
        return self._horizontal_offset

    @property
    def vertical_offset(self) -> float:
        return self._vertical_offset

    def export_json(self) -> Dict[str, Any]:
        return {
            "color": self._color,
            "style": self._style,
            "alpha": self._alpha,
            "round_radius": self._round_radius,
            "height": self._height,
            "width": self._width,
            "horizontal_offset": self._horizontal_offset,
            "vertical_offset": self._vertical_offset,
        }
