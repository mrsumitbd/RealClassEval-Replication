from typing import Any, Callable, Optional
from wave_lang.support.ir_imports import Block, DictAttr, FunctionType, IndexType, InsertionPoint, IntegerAttr, IrType, Location, StringAttr, Value, arith_d, func_d, iree_codegen_d, stream_d

class WorkgroupBuilder:
    """Builder for a workgroup calculation block."""
    __slots__ = ['entry_block', 'workload', '_term_ctor']

    def __init__(self, entry_block: Block, term_ctor: Callable[[list[Value]], None]):
        self.entry_block = entry_block
        self.workload = list(entry_block.arguments)
        self._term_ctor = term_ctor

    @property
    def location(self) -> Location:
        return self.entry_block.owner.location

    def terminate(self, returns: list[Value]):
        entry_block = self.entry_block
        with entry_block.owner.location, InsertionPoint(entry_block):
            self._term_ctor(returns)