from typing import Dict


class Message:

    def __init__(self, role: str, content: str):
        if not isinstance(role, str):
            raise TypeError("role must be a string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        if "role" not in data or "content" not in data:
            raise ValueError("data must contain 'role' and 'content' keys")
        role = data["role"]
        content = data["content"]
        if not isinstance(role, str) or not isinstance(content, str):
            raise TypeError("'role' and 'content' must be strings")
        return cls(role=role, content=content)
