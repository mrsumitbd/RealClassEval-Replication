
from typing import Dict


class Message:

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {'role': self.role, 'content': self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        return cls(data['role'], data['content'])
