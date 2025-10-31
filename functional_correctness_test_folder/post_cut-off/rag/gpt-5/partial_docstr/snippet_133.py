from typing import Tuple, Dict, Any


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, float(value)))


class Text_border:
    '''文本描边的参数'''

    def __init__(
        self,
        *,
        alpha: float = 1.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        width: float = 40.0
    ):
        '''
        Args:
            alpha (`float`, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (`Tuple[float, float, float]`, optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (`float`, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        '''
        if not isinstance(alpha, (int, float)):
            raise TypeError("alpha must be a number.")
        self.alpha: float = _clamp(alpha, 0.0, 1.0)

        if not hasattr(color, "__iter__"):
            raise TypeError("color must be an iterable of three numbers.")
        color_list = list(color)
        if len(color_list) != 3:
            raise ValueError(
                "color must have exactly three components (r, g, b).")
        r, g, b = (float(color_list[0]), float(
            color_list[1]), float(color_list[2]))
        self.color: Tuple[float, float, float] = (
            _clamp(r, 0.0, 1.0),
            _clamp(g, 0.0, 1.0),
            _clamp(b, 0.0, 1.0),
        )

        if not isinstance(width, (int, float)):
            raise TypeError("width must be a number.")
        self.width: float = _clamp(width, 0.0, 100.0)

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        r, g, b = self.color
        return {
            "text_border": {
                "alpha": self.alpha,
                "color": [r, g, b],
                "width": self.width,
            }
        }
