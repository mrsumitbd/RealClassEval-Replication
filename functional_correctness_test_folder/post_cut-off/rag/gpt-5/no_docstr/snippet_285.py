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
        self.block_type = str(block_type) if block_type is not None else ''
        self.content = str(content) if content is not None else ''
        self.title = title if title is None or isinstance(
            title, str) else str(title)

    def __repr__(self) -> str:
        '''Return string representation of the block.
        Returns:
            String representation of the block with its type
            and title if present
        '''
        if self.title:
            return f"<Block type={self.block_type!r} title={self.title!r}>"
        return f"<Block type={self.block_type!r}>"
