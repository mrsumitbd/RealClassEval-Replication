from typing import Any, Dict, List, Optional, Union

class ShadeTimeline:

    def __init__(self, refMemoryId: int=None, createTime: str='', descSecondView: str='', descThirdView: str='', is_new: bool=False):
        self.create_time = createTime
        self.ref_memory_id = refMemoryId
        self.desc_second_view = descSecondView
        self.desc_third_view = descThirdView
        self.is_new = is_new

    @classmethod
    def from_raw_format(cls, raw_format: Dict[str, Any]):
        return cls(refMemoryId=raw_format.get('refMemoryId', None), createTime=raw_format.get('createTime', ''), descSecondView='', descThirdView=raw_format.get('description', ''), is_new=True)

    def add_second_view(self, description):
        self.desc_second_view = description

    def to_json(self):
        return {'createTime': self.create_time, 'refMemoryId': self.ref_memory_id, 'descThirdView': self.desc_third_view, 'descSecondView': self.desc_second_view}