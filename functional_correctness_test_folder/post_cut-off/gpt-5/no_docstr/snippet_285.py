from typing import Optional


class Block:

    def __init__(self, block_type: str, content: str, title: Optional[str] = None):
        if not isinstance(block_type, str) or not block_type:
            raise ValueError("block_type must be a non-empty string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if title is not None and not isinstance(title, str):
            raise TypeError("title must be a string or None")
        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        return f"Block(block_type={self.block_type!r}, content={self.content!r}, title={self.title!r})"
