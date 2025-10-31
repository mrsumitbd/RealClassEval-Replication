import uuid
from typing import Dict, List, Any

class Keyframe:
    """一个关键帧（关键点）, 目前只支持线性插值"""
    kf_id: str
    '关键帧全局id, 自动生成'
    time_offset: int
    '相对于素材起始点的时间偏移量'
    values: List[float]
    '关键帧的值, 似乎一般只有一个元素'

    def __init__(self, time_offset: int, value: float):
        """给定时间偏移量及关键值, 初始化关键帧"""
        self.kf_id = uuid.uuid4().hex
        self.time_offset = time_offset
        self.values = [value]

    def export_json(self) -> Dict[str, Any]:
        return {'curveType': 'Line', 'graphID': '', 'left_control': {'x': 0.0, 'y': 0.0}, 'right_control': {'x': 0.0, 'y': 0.0}, 'id': self.kf_id, 'time_offset': self.time_offset, 'values': self.values}