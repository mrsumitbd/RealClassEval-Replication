from typing import Tuple, Dict, Any


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
            raise TypeError("alpha must be a float")
        if not (0.0 <= float(alpha) <= 1.0):
            raise ValueError("alpha must be in [0, 1]")
        return float(alpha)

    @staticmethod
    def _validate_color(color: Tuple[float, float, float]) -> Tuple[float, float, float]:
        if (
            not isinstance(color, tuple)
            or len(color) != 3
            or not all(isinstance(c, (int, float)) for c in color)
        ):
            raise TypeError("color must be a tuple of three floats")
        r, g, b = (float(color[0]), float(color[1]), float(color[2]))
        for c in (r, g, b):
            if not (0.0 <= c <= 1.0):
                raise ValueError("each color component must be in [0, 1]")
        return (r, g, b)

    @staticmethod
    def _validate_width(width: float) -> float:
        if not isinstance(width, (int, float)):
            raise TypeError("width must be a float")
        if not (0.0 <= float(width) <= 100.0):
            raise ValueError("width must be in [0, 100]")
        return float(width)

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        return {
            "alpha": self.alpha,
            "color": [self.color[0], self.color[1], self.color[2]],
            "width": self.width,
        }
