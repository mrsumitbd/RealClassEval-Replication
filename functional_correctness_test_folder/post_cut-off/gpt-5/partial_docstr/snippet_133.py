from typing import Dict, Any, Tuple


class Text_border:
    '''文本描边的参数'''

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0), width: float = 0.0):
        if not isinstance(alpha, (int, float)):
            raise TypeError("alpha must be a number")
        if not (0.0 <= float(alpha) <= 1.0):
            raise ValueError("alpha must be between 0.0 and 1.0")
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise TypeError("color must be a tuple/list of three floats")
        r, g, b = color
        for c in (r, g, b):
            if not isinstance(c, (int, float)):
                raise TypeError("color components must be numbers")
            if not (0.0 <= float(c) <= 1.0):
                raise ValueError(
                    "color components must be between 0.0 and 1.0")
        if not isinstance(width, (int, float)):
            raise TypeError("width must be a number")
        if float(width) < 0.0:
            raise ValueError("width must be non-negative")

        self.alpha: float = float(alpha)
        self.color: Tuple[float, float, float] = (float(r), float(g), float(b))
        self.width: float = float(width)

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        return {
            "type": "text_border",
            "alpha": self.alpha,
            "color": [self.color[0], self.color[1], self.color[2]],
            "width": self.width,
        }
