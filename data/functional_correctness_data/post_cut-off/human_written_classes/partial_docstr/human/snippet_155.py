import uuid
from typing import Dict, Tuple, Any, List

class TextBubble:
    """文本气泡素材, 与滤镜素材本质上一致"""
    global_id: str
    '气泡全局id, 由程序自动生成'
    effect_id: str
    resource_id: str

    def __init__(self, effect_id: str, resource_id: str):
        self.global_id = uuid.uuid4().hex
        self.effect_id = effect_id
        self.resource_id = resource_id

    def export_json(self) -> Dict[str, Any]:
        return {'apply_target_type': 0, 'effect_id': self.effect_id, 'id': self.global_id, 'resource_id': self.resource_id, 'type': 'text_shape', 'value': 1.0}