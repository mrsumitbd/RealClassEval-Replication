
from typing import Tuple, Dict, Any


class Text_border:
    '''文本描边的参数'''

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0), width: float = 1.0):
        self.alpha = alpha
        self.color = color
        self.width = width

    def export_json(self) -> Dict[str, Any]:
        '''导出JSON数据, 放置在素材content的styles中'''
        return {
            "alpha": self.alpha,
            "color": self.color,
            "width": self.width
        }
