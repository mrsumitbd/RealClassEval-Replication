
from __future__ import annotations

from typing import Any, Dict


class Text_shadow:
    """文本阴影参数"""

    def __init__(
        self,
        *,
        has_shadow: bool = False,
        alpha: float = 0.9,
        angle: float = -45.0,
        color: str = "#000000",
        distance: float = 5.0,
        smoothing: float = 0.45,
    ):
        """
        Args:
            has_shadow (`bool`, optional): 是否启用阴影，默认为False
            alpha (`float`, optional): 阴影不透明度，取值范围[0, 1]，默认为0.9
            angle (`float`, optional): 阴影角度，取值范围[-180, 180], 默认为-45.0
            color (`str`, optional): 阴影颜色，格式为'#RRGGBB'，默认为黑色
            distance (`float`, optional): 阴影距离，默认为5.0
            smoothing (`float`, optional): 阴影平滑度，取值范围[0, 1], 默认0.15
        """
        self.has_shadow = bool(has_shadow)

        if not (0.0 <= alpha <= 1.0):
            raise ValueError(f"alpha must be in [0, 1], got {alpha!r}")
        self.alpha = float(alpha)

        if not (-180.0 <= angle <= 180.0):
            raise ValueError(f"angle must be in [-180, 180], got {angle!r}")
        self.angle = float(angle)

        if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
            raise ValueError(
                f"color must be a hex string '#RRGGBB', got {color!r}")
        # Normalize to uppercase
        self.color = color.upper()

        self.distance = float(distance)

        if not (0.0 <= smoothing <= 1.0):
            raise ValueError(f"smoothing must be in [0, 1], got {smoothing!r}")
        self.smoothing = float(smoothing)

    def export_json(self) -> Dict[str, Any]:
        """生成子JSON数据，在Text_segment导出时合并到其中"""
        if not self.has_shadow:
            return {}
        return {
            "has_shadow": self.has_shadow,
            "alpha": self.alpha,
            "angle": self.angle,
            "color": self.color,
            "distance": self.distance,
            "smoothing": self.smoothing,
        }
