from typing import Any, Dict
import re


class Text_shadow:
    '''文本阴影参数'''

    _COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")

    def __init__(self, *, has_shadow: bool = False, alpha: float = 0.9, angle: float = -45.0,
                 color: str = '#000000', distance: float = 5.0, smoothing: float = 0.45):
        '''
        Args:
            has_shadow (`bool`, optional): 是否启用阴影，默认为False
            alpha (`float`, optional): 阴影不透明度，取值范围[0, 1]，默认为0.9
            angle (`float`, optional): 阴影角度，取值范围[-180, 180], 默认为-45.0
            color (`str`, optional): 阴影颜色，格式为'#RRGGBB'，默认为黑色
            distance (`float`, optional): 阴影距离，默认为5.0
            smoothing (`float`, optional): 阴影平滑度，取值范围[0, 1], 默认0.15
        '''
        if not isinstance(has_shadow, bool):
            raise TypeError("has_shadow must be a boolean")
        if not isinstance(alpha, (int, float)):
            raise TypeError("alpha must be a number")
        if not (0.0 <= float(alpha) <= 1.0):
            raise ValueError("alpha must be in range [0, 1]")
        if not isinstance(angle, (int, float)):
            raise TypeError("angle must be a number")
        if not (-180.0 <= float(angle) <= 180.0):
            raise ValueError("angle must be in range [-180, 180]")
        if not isinstance(color, str):
            raise TypeError("color must be a string")
        if not self._COLOR_PATTERN.match(color):
            raise ValueError("color must be in format '#RRGGBB'")
        if not isinstance(distance, (int, float)):
            raise TypeError("distance must be a number")
        if float(distance) < 0.0:
            raise ValueError("distance must be >= 0")
        if not isinstance(smoothing, (int, float)):
            raise TypeError("smoothing must be a number")
        if not (0.0 <= float(smoothing) <= 1.0):
            raise ValueError("smoothing must be in range [0, 1]")

        self.has_shadow: bool = has_shadow
        self.alpha: float = float(alpha)
        self.angle: float = float(angle)
        self.color: str = color
        self.distance: float = float(distance)
        self.smoothing: float = float(smoothing)

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据，在Text_segment导出时合并到其中'''
        return {
            "has_shadow": self.has_shadow,
            "alpha": self.alpha,
            "angle": self.angle,
            "color": self.color,
            "distance": self.distance,
            "smoothing": self.smoothing,
        }
