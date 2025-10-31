from typing import Literal, Dict, Any
import re


class Text_background:
    '''文本背景参数'''

    _COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

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
        self.color = self._validate_color(color)
        self.style = self._validate_style(style)
        self.alpha = self._validate_range(alpha, "alpha")
        self.round_radius = self._validate_range(round_radius, "round_radius")
        self.height = self._validate_range(height, "height")
        self.width = self._validate_range(width, "width")
        self.horizontal_offset = self._validate_range(
            horizontal_offset, "horizontal_offset")
        self.vertical_offset = self._validate_range(
            vertical_offset, "vertical_offset")

    def _validate_color(self, color: str) -> str:
        if not isinstance(color, str):
            raise TypeError("color must be a string in format '#RRGGBB'")
        if not self._COLOR_RE.match(color):
            raise ValueError("color must match format '#RRGGBB'")
        return color.upper()

    def _validate_style(self, style: int) -> int:
        if style not in (1, 2):
            raise ValueError("style must be 1 or 2")
        return style

    def _validate_range(self, value: float, name: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        value = float(value)
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{name} must be in range [0, 1]")
        return value

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据, 在Text_segment导出时合并到其中'''
        return {
            "color": self.color,
            "style": self.style,
            "alpha": self.alpha,
            "round_radius": self.round_radius,
            "height": self.height,
            "width": self.width,
            "horizontal_offset": self.horizontal_offset,
            "vertical_offset": self.vertical_offset,
        }
