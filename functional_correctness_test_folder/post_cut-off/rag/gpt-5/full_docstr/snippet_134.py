from typing import Any, Dict
import math
import re


class Text_shadow:
    '''文本阴影参数'''

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
        self.has_shadow = bool(has_shadow)
        self.alpha = self._validate_ratio(alpha, 'alpha')
        self.angle = self._validate_angle(angle)
        self.color = self._validate_color(color)
        self.distance = self._validate_distance(distance)
        self.smoothing = self._validate_ratio(smoothing, 'smoothing')

    @staticmethod
    def _validate_ratio(value: float, name: str) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise TypeError(f'{name} must be a float in [0, 1], got {value!r}')
        if not math.isfinite(v) or not (0.0 <= v <= 1.0):
            raise ValueError(f'{name} must be within [0, 1], got {v}')
        return v

    @staticmethod
    def _validate_angle(value: float) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise TypeError(
                f'angle must be a float in [-180, 180], got {value!r}')
        if not math.isfinite(v) or v < -180.0 or v > 180.0:
            raise ValueError(f'angle must be within [-180, 180], got {v}')
        return v

    @staticmethod
    def _validate_distance(value: float) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise TypeError(
                f'distance must be a non-negative float, got {value!r}')
        if not math.isfinite(v) or v < 0.0:
            raise ValueError(f'distance must be a non-negative float, got {v}')
        return v

    @staticmethod
    def _validate_color(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f'color must be a string in format #RRGGBB, got {value!r}')
        if not re.fullmatch(r'#([0-9a-fA-F]{6})', value):
            raise ValueError(f'color must be in format #RRGGBB, got {value!r}')
        return value.upper()

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据，在Text_segment导出时合并到其中'''
        return {
            "shadow": {
                "enable": self.has_shadow,
                "alpha": self.alpha,
                "angle": self.angle,
                "color": self.color,
                "distance": self.distance,
                "smoothing": self.smoothing,
            }
        }
