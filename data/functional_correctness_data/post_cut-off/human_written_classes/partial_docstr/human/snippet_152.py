from typing import Dict, Any

class Crop_settings:
    """素材的裁剪设置, 各属性均在0-1之间, 注意素材的坐标原点在左上角"""
    upper_left_x: float
    upper_left_y: float
    upper_right_x: float
    upper_right_y: float
    lower_left_x: float
    lower_left_y: float
    lower_right_x: float
    lower_right_y: float

    def __init__(self, *, upper_left_x: float=0.0, upper_left_y: float=0.0, upper_right_x: float=1.0, upper_right_y: float=0.0, lower_left_x: float=0.0, lower_left_y: float=1.0, lower_right_x: float=1.0, lower_right_y: float=1.0):
        """初始化裁剪设置, 默认参数表示不裁剪"""
        self.upper_left_x = upper_left_x
        self.upper_left_y = upper_left_y
        self.upper_right_x = upper_right_x
        self.upper_right_y = upper_right_y
        self.lower_left_x = lower_left_x
        self.lower_left_y = lower_left_y
        self.lower_right_x = lower_right_x
        self.lower_right_y = lower_right_y

    def export_json(self) -> Dict[str, Any]:
        return {'upper_left_x': self.upper_left_x, 'upper_left_y': self.upper_left_y, 'upper_right_x': self.upper_right_x, 'upper_right_y': self.upper_right_y, 'lower_left_x': self.lower_left_x, 'lower_left_y': self.lower_left_y, 'lower_right_x': self.lower_right_x, 'lower_right_y': self.lower_right_y}