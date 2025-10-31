
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
        """
        Args:
            alpha (float, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (Tuple[float, float, float], optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (float, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        """
        # Validate alpha
        if not (0.0 <= alpha <= 1.0):
            raise ValueError("alpha must be in [0, 1]")
        # Validate color
        if (
            not isinstance(color, tuple)
            or len(color) != 3
            or not all(0.0 <= c <= 1.0 for c in color)
        ):
            raise ValueError("color must be a tuple of three floats in [0, 1]")
        # Validate width
        if not (0.0 <= width <= 100.0):
            raise ValueError("width must be in [0, 100]")

        self.alpha = alpha
        self.color = color
        self.width = width

    def export_json(self) -> Dict[str, Any]:
        """导出JSON数据, 放置在素材content的styles中"""
        return {
            "alpha": self.alpha,
            "color": list(self.color),
            "width": self.width,
        }
