from typing import Any, Dict, Tuple, Sequence


class Text_border:
    def __init__(
        self,
        *,
        alpha: float = 1.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        width: float = 1.0,
    ):
        self.alpha = self._validate_alpha(alpha)
        self.color = self._validate_color(color)
        self.width = self._validate_width(width)

    def _validate_alpha(self, alpha: float) -> float:
        if not isinstance(alpha, (int, float)):
            raise TypeError("alpha must be a number")
        alpha_f = float(alpha)
        if not (0.0 <= alpha_f <= 1.0):
            raise ValueError("alpha must be between 0.0 and 1.0")
        return alpha_f

    def _validate_color(self, color: Sequence[float]) -> Tuple[float, float, float]:
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise TypeError("color must be a tuple or list of three floats")
        r, g, b = (float(c) for c in color)
        for v in (r, g, b):
            if not (0.0 <= v <= 1.0):
                raise ValueError(
                    "each color component must be between 0.0 and 1.0")
        return (r, g, b)

    def _validate_width(self, width: float) -> float:
        if not isinstance(width, (int, float)):
            raise TypeError("width must be a number")
        w = float(width)
        if w < 0.0:
            raise ValueError("width must be non-negative")
        return w

    def export_json(self) -> Dict[str, Any]:
        return {
            "alpha": self.alpha,
            "color": [self.color[0], self.color[1], self.color[2]],
            "width": self.width,
        }
