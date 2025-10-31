
from typing import Optional


class Block:

    def __init__(self, block_type: str, content: str, title: Optional[str] = None):
        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        if self.title is None:
            return f"Block('{self.block_type}', '{self.content}')"
        else:
            return f"Block('{self.block_type}', '{self.content}', '{self.title}')"
