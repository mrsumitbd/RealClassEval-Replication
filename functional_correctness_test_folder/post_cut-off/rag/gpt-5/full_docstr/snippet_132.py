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
        self._color = self._normalize_color(color)
        if style not in (1, 2):
            raise ValueError("style must be 1 or 2")
        self._style: Literal[1, 2] = style
        self._alpha = self._clamp01(alpha, "alpha")
        self._round_radius = self._clamp01(round_radius, "round_radius")
        self._height = self._clamp01(height, "height")
        self._width = self._clamp01(width, "width")
        self._horizontal_offset = self._clamp01(
            horizontal_offset, "horizontal_offset")
        self._vertical_offset = self._clamp01(
            vertical_offset, "vertical_offset")

    @staticmethod
    def _clamp01(value: float, name: str) -> float:
        try:
            v = float(value)
        except Exception as e:
            raise TypeError(f"{name} must be a float") from e
        if v < 0.0 or v > 1.0:
            raise ValueError(f"{name} must be within [0, 1]")
        return v

    @staticmethod
    def _normalize_color(color: str) -> str:
        if not isinstance(color, str):
            raise TypeError("color must be a string like '#RRGGBB'")
        c = color.strip()
        if c.startswith("#"):
            c = c[1:]
        if len(c) != 6:
            raise ValueError("color must be in '#RRGGBB' format")
        try:
            int(c, 16)
        except ValueError as e:
            raise ValueError("color must be hex in '#RRGGBB' format") from e
        return "#" + c.upper()

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据, 在Text_segment导出时合并到其中'''
        return {
            "color": self._color,
            "style": self._style,
            "alpha": self._alpha,
            "round_radius": self._round_radius,
            "height": self._height,
            "width": self._width,
            "horizontal_offset": self._horizontal_offset,
            "vertical_offset": self._vertical_offset,
        }
