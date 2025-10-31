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
        if not isinstance(block_type, str) or not block_type:
            raise ValueError("block_type must be a non-empty string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        if title is not None and not isinstance(title, str):
            raise ValueError("title must be a string if provided")

        self.block_type: str = block_type
        self.content: str = content
        self.title: Optional[str] = title

    def __repr__(self) -> str:
        '''Return string representation of the block.
        Returns:
            String representation of the block with its type
            and title if present
        '''
        base = f"Block(type={self.block_type!r}"
        if self.title is not None:
            base += f", title={self.title!r}"
        base += ")"
        return base
