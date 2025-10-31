from typing import Dict, Any


class Text_shadow:
    def __init__(
        self,
        *,
        has_shadow: bool = False,
        alpha: float = 0.9,
        angle: float = -45.0,
        color: str = "#000000",
        distance: float = 5.0,
        smoothing: float = 0.45,
    ):
        self.has_shadow = bool(has_shadow)
        self.alpha = self._validate_range(float(alpha), 0.0, 1.0, "alpha")
        self.angle = float(angle)
        self.color = self._validate_color(color)
        self.distance = self._validate_min(float(distance), 0.0, "distance")
        self.smoothing = self._validate_range(
            float(smoothing), 0.0, 1.0, "smoothing")

    def export_json(self) -> Dict[str, Any]:
        return {
            "has_shadow": self.has_shadow,
            "alpha": self.alpha,
            "angle": self.angle,
            "color": self.color,
            "distance": self.distance,
            "smoothing": self.smoothing,
        }

    @staticmethod
    def _validate_range(value: float, min_v: float, max_v: float, name: str) -> float:
        if not (min_v <= value <= max_v):
            raise ValueError(
                f"{name} must be between {min_v} and {max_v}, got {value}")
        return value

    @staticmethod
    def _validate_min(value: float, min_v: float, name: str) -> float:
        if value < min_v:
            raise ValueError(f"{name} must be >= {min_v}, got {value}")
        return value

    @staticmethod
    def _validate_color(color: str) -> str:
        if not isinstance(color, str):
            raise TypeError("color must be a string")
        if not color.startswith("#"):
            raise ValueError("color must start with '#'")
        hex_part = color[1:]
        if len(hex_part) not in (3, 6):
            raise ValueError("color must be in #RGB or #RRGGBB format")
        try:
            int(hex_part, 16)
        except ValueError as e:
            raise ValueError(
                "color contains non-hexadecimal characters") from e
        return color
