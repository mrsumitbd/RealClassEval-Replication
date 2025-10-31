from wave_lang.support.ir_imports import F32Type, F64Type, IndexType, IntegerType, IrType, Location, RankedTensorType, ShapedType, Value
from collections.abc import Sequence
from typing import Any, Callable, List, Optional

class Intrinsic:
    """Objects which interact natively with the tracing system implement this."""
    __slots__: List[str] = []

    def resolve_ir_values(self, proc_trace: 'IrTrace') -> Sequence[Value]:
        raise NotImplementedError(f'Cannot use {self} as an expression in a procedural function')

    def resolve_call(self, proc_trace: 'IrTrace', *args, **kwargs):
        raise NotImplementedError(f'Cannot use {self} as the target of a call in a procedural function')

    def resolve_assignment(self, proc_trace: 'IrTrace', ir_values: Sequence[Value]):
        raise NotImplementedError(f'Cannot use {self} as the target of an assignment in a procedural function')

    @property
    def ir_values(self) -> Sequence[Value]:
        return self.resolve_ir_values(current_ir_trace())

    @property
    def ir_value(self) -> Value:
        values = self.ir_values
        assert len(values) == 1, 'Expected arity one intrinsic'
        return values[0]