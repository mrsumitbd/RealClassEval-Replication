
from typing import Tuple, Dict, Any


class Text_border:
    '''文本描边的参数'''

    def __init__(
        self,
        *,
        alpha: float = 1.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        width: float = 40.0,
    ):
        """
        Args:
            alpha (float, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (Tuple[float, float, float], optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (float, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        """
        self.alpha = float(alpha)
        self.color = tuple(float(c) for c in color)
        self.width = float(width)

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        return {
            "alpha": self.alpha,
            "color": self.color,
            "width": self.width,
        }
