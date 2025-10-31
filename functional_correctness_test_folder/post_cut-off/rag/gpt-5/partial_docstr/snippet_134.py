from typing import Dict, Any


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
        if not isinstance(has_shadow, bool):
            raise TypeError('has_shadow must be a bool')
        try:
            alpha_val = float(alpha)
        except (TypeError, ValueError):
            raise TypeError('alpha must be a float')
        if not (0.0 <= alpha_val <= 1.0):
            raise ValueError('alpha must be between 0 and 1')

        try:
            angle_val = float(angle)
        except (TypeError, ValueError):
            raise TypeError('angle must be a float')
        if not (-180.0 <= angle_val <= 180.0):
            raise ValueError('angle must be between -180 and 180')

        if not isinstance(color, str):
            raise TypeError('color must be a string')
        color_str = color.strip()
        if not (len(color_str) == 7 and color_str.startswith('#')):
            raise ValueError("color must be in format '#RRGGBB'")
        hex_part = color_str[1:]
        try:
            int(hex_part, 16)
        except ValueError:
            raise ValueError(
                "color must be in format '#RRGGBB' with valid hex digits")
        # Normalize to uppercase hex
        color_str = '#' + hex_part.upper()

        try:
            distance_val = float(distance)
        except (TypeError, ValueError):
            raise TypeError('distance must be a float')
        if distance_val < 0:
            raise ValueError('distance must be non-negative')

        try:
            smoothing_val = float(smoothing)
        except (TypeError, ValueError):
            raise TypeError('smoothing must be a float')
        if not (0.0 <= smoothing_val <= 1.0):
            raise ValueError('smoothing must be between 0 and 1')

        self.has_shadow: bool = has_shadow
        self.alpha: float = alpha_val
        self.angle: float = angle_val
        self.color: str = color_str
        self.distance: float = distance_val
        self.smoothing: float = smoothing_val

    def export_json(self) -> Dict[str, Any]:
        '''生成子JSON数据，在Text_segment导出时合并到其中'''
        return {
            'has_shadow': self.has_shadow,
            'alpha': self.alpha,
            'angle': self.angle,
            'color': self.color,
            'distance': self.distance,
            'smoothing': self.smoothing,
        }
