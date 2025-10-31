from torch import Tensor
from typing import Any, Callable, Optional, Sequence, Type, Union, cast

class EmptyOptionalTensorArg:
    """Sentinel type marking an optional tensor argument that was not provided
    at the call site.

    To `KernelSelection` a `None` `ArgDescriptor` indicates an argument has been
    declared as part of the signature, but the `ArgDescriptor` hasn't been
    initialized with values an actual call site. An `EmptyOptionalTensorArg`
    signals that an `ArgDescriptor` has been initialized, but an argument was
    not provided at the call site.
    """
    ir_arity: int = 0
    maybe_tensor_value: Optional[Tensor] = None
    is_list: bool = False

    def __repr__(self):
        return 'TensorArg(None)'

    @property
    def spec_key(self) -> str:
        return 'TensorArg(None)'

    @property
    def mlir_type_asm(self) -> str:
        raise AssertionError('EmptyOptionalTensorArg has no mlir_type_asm')

    def generate_meta(self) -> None:
        return None