
from typing import Optional


class Block:

    def __init__(self, block_type: str, content: str, title: Optional[str] = None):
        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        title_str = f", title='{self.title}'" if self.title is not None else ""
        return f"Block(block_type='{self.block_type}', content='{self.content}'{title_str})"
