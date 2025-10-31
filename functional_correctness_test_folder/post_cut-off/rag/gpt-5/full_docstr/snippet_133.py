from typing import Tuple, Dict, Any, Sequence


class Text_border:
    '''文本描边的参数'''

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0), width: float = 40.0):
        '''
        Args:
            alpha (`float`, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (`Tuple[float, float, float]`, optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (`float`, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        '''
        self.alpha = self._validate_alpha(alpha)
        self.color = self._validate_color(color)
        self.width = self._validate_width(width)

    @staticmethod
    def _validate_alpha(alpha: float) -> float:
        if not isinstance(alpha, (int, float)):
            raise TypeError("alpha must be a number.")
        alpha = float(alpha)
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be in [0, 1].")
        return alpha

    @staticmethod
    def _validate_color(color: Sequence[float]) -> Tuple[float, float, float]:
        if not isinstance(color, (list, tuple)) or len(color) != 3:
            raise TypeError(
                "color must be a 3-tuple/list of floats in [0, 1].")
        r, g, b = color
        for v in (r, g, b):
            if not isinstance(v, (int, float)):
                raise TypeError("color components must be numbers.")
            fv = float(v)
            if not 0.0 <= fv <= 1.0:
                raise ValueError("color components must be in [0, 1].")
        return float(r), float(g), float(b)

    @staticmethod
    def _validate_width(width: float) -> float:
        if not isinstance(width, (int, float)):
            raise TypeError("width must be a number.")
        width = float(width)
        if not 0.0 <= width <= 100.0:
            raise ValueError("width must be in [0, 100].")
        return width

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        return {
            "type": "text_border",
            "alpha": self.alpha,
            "color": {
                "r": self.color[0],
                "g": self.color[1],
                "b": self.color[2],
            },
            "width": self.width,
        }
