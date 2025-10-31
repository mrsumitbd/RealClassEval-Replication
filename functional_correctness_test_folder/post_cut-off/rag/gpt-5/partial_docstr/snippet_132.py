from typing import Any, Dict, Literal


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
        self.color = self._validate_color(color)
        if style not in (1, 2):
            raise ValueError("style must be 1 or 2")
        self.style: Literal[1, 2] = style

        self.alpha = self._clamp01(alpha, "alpha")
        self.round_radius = self._clamp01(round_radius, "round_radius")
        self.height = self._clamp01(height, "height")
        self.width = self._clamp01(width, "width")
        self.horizontal_offset = self._clamp01(
            horizontal_offset, "horizontal_offset")
        self.vertical_offset = self._clamp01(
            vertical_offset, "vertical_offset")

    @staticmethod
    def _clamp01(value: float, name: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if value < 0.0:
            return 0.0
        if value > 1.0:
            return 1.0
        return float(value)

    @staticmethod
    def _validate_color(color: str) -> str:
        if not isinstance(color, str):
            raise TypeError("color must be a string in format '#RRGGBB'")
        if len(color) != 7 or not color.startswith("#"):
            raise ValueError("color must be in format '#RRGGBB'")
        hex_part = color[1:]
        try:
            int(hex_part, 16)
        except ValueError as e:
            raise ValueError("color must be in format '#RRGGBB'") from e
        return "#" + hex_part.upper()

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据, 在Text_segment导出时合并到其中'''
        return {
            "text_background": {
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
