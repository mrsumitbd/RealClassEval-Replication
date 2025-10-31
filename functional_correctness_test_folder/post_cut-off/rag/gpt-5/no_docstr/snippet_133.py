from typing import Any, Dict, Tuple


class Text_border:
    '''文本描边的参数'''

    def __init__(
        self,
        *,
        alpha: float = 1.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        width: float = 40.0,
    ):
        '''
        Args:
            alpha (`float`, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (`Tuple[float, float, float]`, optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (`float`, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        '''
        self.alpha = max(0.0, min(1.0, float(alpha)))
        if isinstance(color, (list, tuple)) and len(color) == 3:
            r, g, b = (float(color[0]), float(color[1]), float(color[2]))
        else:
            raise ValueError(
                "color must be a 3-tuple/list of floats in [0, 1].")
        self.color: Tuple[float, float, float] = (
            max(0.0, min(1.0, r)),
            max(0.0, min(1.0, g)),
            max(0.0, min(1.0, b)),
        )
        self.width = max(0.0, min(100.0, float(width)))

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        r, g, b = self.color
        return {
            "text_border": {
                "alpha": self.alpha,
                "color": {"r": r, "g": g, "b": b},
                "width": self.width,
            }
        }
