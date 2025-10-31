from torch import Tensor
from typing import Any, Callable, Optional, Sequence, Type, Union, cast

class AttrArg:
    ir_arity: int = 0
    maybe_tensor_value: Optional[Tensor] = None
    is_list: bool = False
    __slots__ = ['v', 'spec_value']

    def __init__(self, v: object):
        self.v = v
        self.spec_value: Optional[Any] = v

    def __repr__(self):
        return f'AttrArg(<{self.spec_value}>)'

    def generate_meta(self) -> object:
        return self.v

    @property
    def spec_key(self) -> str:
        """Generates a key that will be the same for all specializations."""
        return f'attr<{self.spec_value}>'

    @property
    def mlir_type_asm(self) -> str:
        raise AssertionError('Cannot resolve `mlir_type_asm` for an AttrArg')