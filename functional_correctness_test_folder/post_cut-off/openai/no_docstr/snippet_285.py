
from typing import Optional


class Block:
    def __init__(self, block_type: str, content: str, title: Optional[str] = None):
        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        return (
            f"Block(block_type={self.block_type!r}, "
            f"content={self.content!r}, title={self.title!r})"
        )
