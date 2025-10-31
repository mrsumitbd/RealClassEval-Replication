
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
        if not isinstance(block_type, str):
            raise TypeError(
                f"block_type must be a str, got {type(block_type).__name__}")
        if not isinstance(content, str):
            raise TypeError(
                f"content must be a str, got {type(content).__name__}")
        if title is not None and not isinstance(title, str):
            raise TypeError(
                f"title must be a str or None, got {type(title).__name__}")

        self.block_type = block_type
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        '''Return string representation of the block.
        Returns:
            String representation of the block with its type
            and title if present
        '''
        if self.title:
            return f"Block(type={self.block_type!r}, title={self.title!r})"
        return f"Block(type={self.block_type!r})"
