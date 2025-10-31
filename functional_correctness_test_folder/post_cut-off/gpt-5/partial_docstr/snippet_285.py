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
        self.content = '' if content is None else str(content)
        self.title = None if title is None else str(title)

    def __repr__(self) -> str:
        def _preview(s: str, limit: int = 60) -> str:
            s = s.replace('\n', '\\n').replace('\r', '\\r')
            return s if len(s) <= limit else s[: max(0, limit - 3)] + '...'
        parts = [f"block_type={self.block_type!r}"]
        if self.title is not None:
            parts.append(f"title={self.title!r}")
        parts.append(f"content={_preview(self.content)!r}")
        return f"Block({', '.join(parts)})"
