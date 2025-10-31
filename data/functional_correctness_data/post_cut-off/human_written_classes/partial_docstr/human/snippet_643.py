from torch import Tensor
from typing import Any, Callable, Optional, Sequence, Type, Union, cast
from wave_lang.support.conversions import TORCH_DTYPE_TO_IREE_TYPE_ASM

class TensorListArg:
    __slots__ = ['ts', 'spec_dims', 'ir_arity', 'maybe_tensor_value']
    is_list: bool = True

    def __init__(self, ts: list[Tensor]):
        self.ts = ts
        self.ir_arity = len(ts)
        self.spec_dims: list[list[Optional[int]]] = [len(t.shape) * [None] for t in ts]
        self.maybe_tensor_value: list[Tensor] = ts

    def __repr__(self):
        return f'TensorListArg(shape={[t.shape for t in self.ts]}, dtype={[t.dtype for t in self.ts]}, spec_dims={self.spec_dims}, ir_arity={self.ir_arity})'

    def generate_meta(self) -> list[Tensor]:
        metas = []
        for t in self.ts:
            if t.device == 'meta':
                metas.append(t)
            else:
                metas.append(t.clone().detach().to('meta'))
        return metas

    @property
    def spec_key(self) -> str:
        """Generates a key that will be the same for all specializations."""
        return f'tensor[{[len(t.shape) for t in self.ts]}:{[str(t.dtype) for t in self.ts]}]<{self.spec_dims}>'

    @property
    def mlir_type_asm(self) -> list[str]:
        asms = []
        for t, spec_dims in zip(self.ts, self.spec_dims):
            try:
                dtype_asm = TORCH_DTYPE_TO_IREE_TYPE_ASM[t.dtype]
            except KeyError as e:
                raise KeyError(f'Unknown mapping of torch dtype {t.dtype} to MLIR (possibly missing in TORCH_DTYPE_TO_IREE_TYPE_ASM table)') from e
            dim_asm = 'x'.join(['?' if d is None else str(d) for d in spec_dims])
            spec = f'{dim_asm}x{dtype_asm}' if dim_asm else dtype_asm
            asms.append(f'tensor<{spec}>')
        return asms