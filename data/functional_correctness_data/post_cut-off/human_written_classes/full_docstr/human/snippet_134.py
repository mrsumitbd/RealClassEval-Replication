from typing import Dict, Tuple, Any, List

class Text_shadow:
    """文本阴影参数"""
    has_shadow: bool
    '是否启用阴影'
    alpha: float
    '阴影不透明度'
    angle: float
    '阴影角度'
    color: str
    "阴影颜色，格式为'#RRGGBB'"
    distance: float
    '阴影距离'
    smoothing: float
    '阴影平滑度'

    def __init__(self, *, has_shadow: bool=False, alpha: float=0.9, angle: float=-45.0, color: str='#000000', distance: float=5.0, smoothing: float=0.45):
        """
        Args:
            has_shadow (`bool`, optional): 是否启用阴影，默认为False
            alpha (`float`, optional): 阴影不透明度，取值范围[0, 1]，默认为0.9
            angle (`float`, optional): 阴影角度，取值范围[-180, 180], 默认为-45.0
            color (`str`, optional): 阴影颜色，格式为'#RRGGBB'，默认为黑色
            distance (`float`, optional): 阴影距离，默认为5.0
            smoothing (`float`, optional): 阴影平滑度，取值范围[0, 1], 默认0.15
        """
        self.has_shadow = has_shadow
        self.alpha = alpha
        self.angle = angle
        self.color = color
        self.distance = distance
        self.smoothing = smoothing

    def export_json(self) -> Dict[str, Any]:
        """生成子JSON数据，在Text_segment导出时合并到其中"""
        return {'has_shadow': self.has_shadow, 'shadow_alpha': self.alpha, 'shadow_angle': self.angle, 'shadow_color': self.color, 'shadow_distance': self.distance, 'shadow_smoothing': self.smoothing * 3}