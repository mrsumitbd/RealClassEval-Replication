
from typing import Optional


class Block:
    '''Represents a block in the Gemini response.
    Blocks are discrete chunks of content with different types
    (text, code, HTML, etc.) returned in a Gemini conversation response.
    '''

    def __init__(self, block_type: str, content: str, title: Optional[str] = None):
        '''Initialize a response block.
        Args:
            block_type: The type of the block ('TEXT', 'CODE', 'HTML', etc.)
            content: The content of the block
            title: Optional title for the block (may be present in CODE blocks)
        '''
        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"block_type={self.block_type!r}, "
            f"content={self.content!r}, "
            f"title={self.title!r})"
        )
