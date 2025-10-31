from typing import Dict, Any
import re


class Text_shadow:

    def __init__(self, *, has_shadow: bool = False, alpha: float = 0.9, angle: float = -45.0, color: str = '#000000', distance: float = 5.0, smoothing: float = 0.45):
        '''
        Args:
            has_shadow (`bool`, optional): 是否启用阴影，默认为False
            alpha (`float`, optional): 阴影不透明度，取值范围[0, 1]，默认为0.9
            angle (`float`, optional): 阴影角度，取值范围[-180, 180], 默认为-45.0
            color (`str`, optional): 阴影颜色，格式为'#RRGGBB'，默认为黑色
            distance (`float`, optional): 阴影距离，默认为5.0
            smoothing (`float`, optional): 阴影平滑度，取值范围[0, 1], 默认0.15
        '''
        self.has_shadow = self._validate_bool(has_shadow, "has_shadow")
        self.alpha = self._validate_range_float(alpha, 0.0, 1.0, "alpha")
        self.angle = self._validate_range_float(angle, -180.0, 180.0, "angle")
        self.color = self._validate_color(color)
        self.distance = self._validate_float(distance, "distance")
        self.smoothing = self._validate_range_float(
            smoothing, 0.0, 1.0, "smoothing")

    @staticmethod
    def _validate_bool(value: Any, name: str) -> bool:
        if not isinstance(value, bool):
            raise TypeError(f"{name} must be a bool.")
        return value

    @staticmethod
    def _validate_float(value: Any, name: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")
        return float(value)

    @staticmethod
    def _validate_range_float(value: Any, min_v: float, max_v: float, name: str) -> float:
        v = Text_shadow._validate_float(value, name)
        if not (min_v <= v <= max_v):
            raise ValueError(f"{name} must be in [{min_v}, {max_v}].")
        return v

    @staticmethod
    def _validate_color(value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("color must be a string.")
        if not re.fullmatch(r"#([0-9a-fA-F]{6})", value):
            raise ValueError("color must match format '#RRGGBB'.")
        return value.lower()

    def export_json(self) -> Dict[str, Any]:
        return {
            "has_shadow": self.has_shadow,
            "alpha": self.alpha,
            "angle": self.angle,
            "color": self.color,
            "distance": self.distance,
            "smoothing": self.smoothing,
        }
