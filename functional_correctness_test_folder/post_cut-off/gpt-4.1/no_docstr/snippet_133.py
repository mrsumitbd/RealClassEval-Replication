
from typing import Tuple, Dict, Any


class Text_border:

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0), width: float = 1.0):
        self.alpha = alpha
        self.color = color
        self.width = width

    def export_json(self) -> Dict[str, Any]:
        return {
            "alpha": self.alpha,
            "color": list(self.color),
            "width": self.width
        }
