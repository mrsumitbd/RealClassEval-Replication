
from typing import Dict


class Message:
    def __init__(self, role: str, content: str):
        if not isinstance(role, str):
            raise TypeError(f"role must be a str, got {type(role).__name__}")
        if not isinstance(content, str):
            raise TypeError(
                f"content must be a str, got {type(content).__name__}")
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Message":
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")
        if "role" not in data or "content" not in data:
            raise ValueError("data must contain 'role' and 'content' keys")
        role = data["role"]
        content = data["content"]
        if not isinstance(role, str):
            raise TypeError(f"role must be a str, got {type(role).__name__}")
        if not isinstance(content, str):
            raise TypeError(
                f"content must be a str, got {type(content).__name__}")
        return cls(role, content)
