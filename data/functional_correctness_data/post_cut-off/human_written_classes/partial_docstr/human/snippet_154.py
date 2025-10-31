from typing import Optional, Dict, List, Any, Union
import uuid

class Speed:
    """播放速度对象, 目前只支持固定速度"""
    global_id: str
    '全局id, 由程序自动生成'
    speed: float
    '播放速度'

    def __init__(self, speed: float):
        self.global_id = uuid.uuid4().hex
        self.speed = speed

    def export_json(self) -> Dict[str, Any]:
        return {'curve_speed': None, 'id': self.global_id, 'mode': 0, 'speed': self.speed, 'type': 'speed'}