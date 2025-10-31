from typing import Dict, Tuple, Any, List
from typing import Union, Optional, Literal

class Text_background:
    """文本背景参数"""
    style: Literal[0, 2]
    '背景样式'
    alpha: float
    '背景不透明度'
    color: str
    "背景颜色, 格式为'#RRGGBB'"
    round_radius: float
    '背景圆角半径'
    height: float
    '背景高度'
    width: float
    '背景宽度'
    horizontal_offset: float
    '背景水平偏移'
    vertical_offset: float
    '背景竖直偏移'

    def __init__(self, *, color: str, style: Literal[1, 2]=1, alpha: float=1.0, round_radius: float=0.0, height: float=0.14, width: float=0.14, horizontal_offset: float=0.5, vertical_offset: float=0.5):
        """
        Args:
            color (`str`): 背景颜色, 格式为'#RRGGBB'
            style (`int`, optional): 背景样式, 1和2分别对应剪映中的两种样式, 默认为1
            alpha (`float`, optional): 背景不透明度, 与剪映中一致, 取值范围[0, 1], 默认为1.0
            round_radius (`float`, optional): 背景圆角半径, 与剪映中一致, 取值范围[0, 1], 默认为0.0
            height (`float`, optional): 背景高度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            width (`float`, optional): 背景宽度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            horizontal_offset (`float`, optional): 背景水平偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
            vertical_offset (`float`, optional): 背景竖直偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
        """
        self.style = (0, 2)[style - 1]
        self.alpha = alpha
        self.color = color
        self.round_radius = round_radius
        self.height = height
        self.width = width
        self.horizontal_offset = horizontal_offset * 2 - 1
        self.vertical_offset = vertical_offset * 2 - 1

    def export_json(self) -> Dict[str, Any]:
        """生成子JSON数据, 在Text_segment导出时合并到其中"""
        return {'background_style': self.style, 'background_color': self.color, 'background_alpha': self.alpha, 'background_round_radius': self.round_radius, 'background_height': self.height, 'background_width': self.width, 'background_horizontal_offset': self.horizontal_offset, 'background_vertical_offset': self.vertical_offset}