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
            raise TypeError('block_type must be a string')
        if not isinstance(content, str):
            raise TypeError('content must be a string')
        if title is not None and not isinstance(title, str):
            raise TypeError('title must be a string or None')

        self.block_type = block_type.upper()
        self.content = content
        self.title = title

    def __repr__(self) -> str:
        '''Return string representation of the block.
        Returns:
            String representation of the block with its type
            and title if present
        '''
        title_part = f" title={self.title!r}" if self.title else ""
        return f"<Block {self.block_type}{title_part}>"
