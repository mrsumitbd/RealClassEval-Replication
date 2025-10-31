from typing import Literal, Dict, Any
import re


class Text_background:
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
        vertical_offset: float = 0.5,
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
        self._validate_color(color)
        self.color = color

        if style not in (1, 2):
            raise ValueError("style must be 1 or 2")
        self.style = style

        self.alpha = self._validate_range(alpha, "alpha", 0.0, 1.0)
        self.round_radius = self._validate_range(
            round_radius, "round_radius", 0.0, 1.0)
        self.height = self._validate_range(height, "height", 0.0, 1.0)
        self.width = self._validate_range(width, "width", 0.0, 1.0)
        self.horizontal_offset = self._validate_range(
            horizontal_offset, "horizontal_offset", 0.0, 1.0)
        self.vertical_offset = self._validate_range(
            vertical_offset, "vertical_offset", 0.0, 1.0)

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据, 在Text_segment导出时合并到其中'''
        return {
            "background": {
                "color": self.color,
                "style": self.style,
                "alpha": self.alpha,
                "round_radius": self.round_radius,
                "height": self.height,
                "width": self.width,
                "horizontal_offset": self.horizontal_offset,
                "vertical_offset": self.vertical_offset,
            }
        }

    @staticmethod
    def _validate_range(value: float, name: str, min_v: float, max_v: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        v = float(value)
        if not (min_v <= v <= max_v):
            raise ValueError(f"{name} must be in [{min_v}, {max_v}]")
        return v

    @staticmethod
    def _validate_color(color: str) -> None:
        if not isinstance(color, str):
            raise TypeError("color must be a string")
        if not re.fullmatch(r"#([0-9A-Fa-f]{6})", color):
            raise ValueError("color must be in format '#RRGGBB'")
