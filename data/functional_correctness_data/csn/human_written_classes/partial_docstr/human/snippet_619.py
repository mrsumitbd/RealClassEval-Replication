class ExceptionTableEntry:
    """Entry for a given line in the exception table.

    All offset are expressed in instructions not in bytes.

    """
    start_offset: int
    stop_offset: int
    target: int
    stack_depth: int
    push_lasti: bool
    __slots__ = ('push_lasti', 'stack_depth', 'start_offset', 'stop_offset', 'target')

    def __init__(self, start_offset: int, stop_offset: int, target: int, stack_depth: int, push_lasti: bool) -> None:
        self.start_offset = start_offset
        self.stop_offset = stop_offset
        self.target = target
        self.stack_depth = stack_depth
        self.push_lasti = push_lasti

    def __repr__(self) -> str:
        return f'ExceptionTableEntry(start_offset={self.start_offset}, stop_offset={self.stop_offset}, target={self.target}, stack_depth={self.stack_depth}, push_lasti={self.push_lasti}'