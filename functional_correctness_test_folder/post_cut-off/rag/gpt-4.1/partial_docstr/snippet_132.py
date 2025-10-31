from typing import Dict, Any, Literal


class Text_background:
    '''文本背景参数'''

    def __init__(
        self,
        *,
        color: str,
        style: Literal[1, 2] = 1,
        alpha: float = 1.0,
        round_radius: float = 0.0,
        height: float = 0.14,
        width: float = 0.14,
        horizontal_offset: float = 0.5,
        vertical_offset: float = 0.5
    ):
        '''
        Args:
            color (`str`): 背景颜色, 格式为'#RRGGBB'
            style (`int`, optional): 背景样式, 1和2分别对应剪映中的两种样式, 默认为1
            alpha (`float`, optional): 背景不透明度, 与剪映中一致, 取值范围[0, 1], 默认为1.0
            round_radius (`float`, optional): 背景圆角半径, 与剪映中一致, 取值范围[0, 1], 默认为0.0
            height (`float`, optional): 背景高度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            width (`float`, optional): 背景宽度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            horizontal_offset (`float`, optional): 背景水平偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
            vertical_offset (`float`, optional): 背景竖直偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
        '''
        self.color = color
        self.style = style
        self.alpha = alpha
        self.round_radius = round_radius
        self.height = height
        self.width = width
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据, 在Text_segment导出时合并到其中'''
        return {
            "Color": self.color,
            "Style": self.style,
            "Alpha": self.alpha,
            "RoundRadius": self.round_radius,
            "Height": self.height,
            "Width": self.width,
            "HorizontalOffset": self.horizontal_offset,
            "VerticalOffset": self.vertical_offset
        }
