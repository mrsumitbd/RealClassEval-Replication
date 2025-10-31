
class CBlock:
    '''A `CBlock` is a block of content that can serve as input to or output from an LLM.'''

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        '''Initializes the CBlock with a string and some metadata.'''
        self._value = value
        self.meta = meta or {}

    @property
    def value(self) -> str | None:
        '''Gets the value of the block.'''
        return self._value

    @value.setter
    def value(self, value: str | None) -> None:
        '''Sets the value of the block.'''
        self._value = value

    def __str__(self):
        '''Stringifies the block.'''
        return str(self._value)

    def __repr__(self):
        '''Provides a python-parsable representation of the block (usually).'''
        return f"CBlock(value={repr(self._value)}, meta={repr(self.meta)})"
