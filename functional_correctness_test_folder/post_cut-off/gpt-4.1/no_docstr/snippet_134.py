
from typing import Dict, Any


class Text_shadow:

    def __init__(self, *, has_shadow: bool = False, alpha: float = 0.9, angle: float = -45.0, color: str = '#000000', distance: float = 5.0, smoothing: float = 0.45):
        self.has_shadow = has_shadow
        self.alpha = alpha
        self.angle = angle
        self.color = color
        self.distance = distance
        self.smoothing = smoothing

    def export_json(self) -> Dict[str, Any]:
        return {
            "has_shadow": self.has_shadow,
            "alpha": self.alpha,
            "angle": self.angle,
            "color": self.color,
            "distance": self.distance,
            "smoothing": self.smoothing
        }
