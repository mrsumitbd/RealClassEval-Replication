import uuid
from typing import Dict, List, Any

class Audio_fade:
    """音频淡入淡出效果"""
    fade_id: str
    '淡入淡出效果的全局id, 自动生成'
    in_duration: int
    '淡入时长, 单位为微秒'
    out_duration: int
    '淡出时长, 单位为微秒'

    def __init__(self, in_duration: int, out_duration: int):
        """根据给定的淡入/淡出时长构造一个淡入淡出效果"""
        self.fade_id = uuid.uuid4().hex
        self.in_duration = in_duration
        self.out_duration = out_duration

    def export_json(self) -> Dict[str, Any]:
        return {'id': self.fade_id, 'fade_in_duration': self.in_duration, 'fade_out_duration': self.out_duration, 'fade_type': 0, 'type': 'audio_fade'}