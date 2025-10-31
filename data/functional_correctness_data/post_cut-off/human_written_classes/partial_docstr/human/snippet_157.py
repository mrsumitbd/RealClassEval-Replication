import uuid
from typing import Dict, List, Tuple, Any
from typing import Optional, Literal, Union, overload

class BackgroundFilling:
    """背景填充对象"""
    global_id: str
    '背景填充全局id, 由程序自动生成'
    fill_type: Literal['canvas_blur', 'canvas_color']
    '背景填充类型'
    blur: float
    '模糊程度, 0-1'
    color: str
    "背景颜色, 格式为'#RRGGBBAA'"

    def __init__(self, fill_type: Literal['canvas_blur', 'canvas_color'], blur: float, color: str):
        self.global_id = uuid.uuid4().hex
        self.fill_type = fill_type
        self.blur = blur
        self.color = color

    def export_json(self) -> Dict[str, Any]:
        return {'id': self.global_id, 'type': self.fill_type, 'blur': self.blur, 'color': self.color, 'source_platform': 0}