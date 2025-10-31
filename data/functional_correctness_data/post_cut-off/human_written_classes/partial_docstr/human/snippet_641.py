from typing import Any, Callable, Optional, Sequence, Type, Union, cast
from torch import Tensor

class IntArg:
    __slots__ = ['ir_arity', 'spec_value', 'v']
    maybe_tensor_value: Optional[Tensor] = None
    is_list: bool = False

    def __init__(self, v: int):
        self.v = v
        self.spec_value: Optional[Any] = None
        self.ir_arity: int = 1

    def __repr__(self):
        return f'IntArg({self.v}, spec_value={self.spec_value}, is_ir_arg={self.is_ir_arg})'

    def generate_meta(self) -> int:
        return self.v

    @property
    def spec_key(self) -> str:
        """Generates a key that will be the same for all specializations."""
        return f'int<{self.spec_value}>'

    @property
    def mlir_type_asm(self) -> str:
        return 'i64'