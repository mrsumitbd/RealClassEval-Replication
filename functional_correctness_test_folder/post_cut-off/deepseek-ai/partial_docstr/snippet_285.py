
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
        title_str = f", title='{self.title}'" if self.title is not None else ""
        return f"Block(block_type='{self.block_type}', content='{self.content[:20]}...'{title_str})"
