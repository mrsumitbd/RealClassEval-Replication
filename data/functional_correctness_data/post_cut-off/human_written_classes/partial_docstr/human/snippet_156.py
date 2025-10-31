from typing import Dict

class Timerange:
    """记录了起始时间及持续长度的时间范围"""
    start: int
    '起始时间, 单位为微秒'
    duration: int
    '持续长度, 单位为微秒'

    def __init__(self, start: int, duration: int):
        """构造一个时间范围

        Args:
            start (int): 起始时间, 单位为微秒
            duration (int): 持续长度, 单位为微秒
        """
        self.start = start
        self.duration = duration

    @classmethod
    def import_json(cls, json_obj: Dict[str, str]) -> 'Timerange':
        """从json对象中恢复Timerange"""
        return cls(int(json_obj['start']), int(json_obj['duration']))

    @property
    def end(self) -> int:
        """结束时间, 单位为微秒"""
        return self.start + self.duration

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timerange):
            return False
        return self.start == other.start and self.duration == other.duration

    def overlaps(self, other: 'Timerange') -> bool:
        """判断两个时间范围是否有重叠"""
        return not (self.end <= other.start or other.end <= self.start)

    def __repr__(self) -> str:
        return f'Timerange(start={self.start}, duration={self.duration})'

    def __str__(self) -> str:
        return f'[start={self.start}, end={self.end}]'

    def export_json(self) -> Dict[str, int]:
        return {'start': self.start, 'duration': self.duration}