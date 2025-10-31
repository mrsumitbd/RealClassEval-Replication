from typing import Any, Dict
from typing_extensions import override

class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __json_encode__(self):
        """Called during serialization"""
        return {'x': self.x, 'y': self.y}

    @classmethod
    def __json_decode__(cls, data: Dict[str, Any]):
        """Called during deserialization"""
        return cls(data['x'], data['y'])

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    @override
    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y})'