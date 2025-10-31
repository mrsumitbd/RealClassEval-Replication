from typing import Any, Dict, List, Optional, Tuple

class P0MetricInfo:
    """P0级监控项信息类"""

    def __init__(self, name: str, meaning: str, description: str, unit: str=''):
        self.name = name
        self.meaning = meaning
        self.description = description
        self.unit = unit

    def to_dict(self) -> Dict[str, str]:
        return {'name': self.name, 'meaning': self.meaning, 'description': self.description, 'unit': self.unit}