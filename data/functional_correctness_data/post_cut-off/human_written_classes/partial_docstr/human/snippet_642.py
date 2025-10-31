from torch import Tensor
from wave_lang.support.conversions import TORCH_DTYPE_TO_IREE_TYPE_ASM

class TensorArg:
    __slots__ = ['t', 'spec_dims', 'maybe_tensor_value']
    ir_arity: int = 1
    is_list: bool = False

    def __init__(self, t: Tensor):
        self.t = t
        self.spec_dims = len(t.shape) * [_NoneInt]
        self.maybe_tensor_value: Tensor = t

    def specialize_all_dims(self):
        """Marks all dimensions as specialized."""
        self.spec_dims = list(self.t.shape)

    def specialize_dims(self, *indices: int):
        """Specializes individual dimensions.

        `i` can have negative indexing.
        """
        for i in indices:
            self.spec_dims[i] = self.t.size(i)

    def __repr__(self):
        return f'TensorArg(shape={self.t.shape}, dtype={self.t.dtype}, spec_dims={self.spec_dims})'

    def generate_meta(self) -> Tensor:
        t = self.t
        if t.device == 'meta':
            return t
        else:
            return t.clone().detach().to('meta')

    @property
    def spec_key(self) -> str:
        """Generates a key that will be the same for all specializations."""
        t = self.t
        return f'tensor[{len(t.shape)}:{str(t.dtype)}]<{self.spec_dims}>'

    @property
    def mlir_type_asm(self) -> str:
        t = self.t
        try:
            dtype_asm = TORCH_DTYPE_TO_IREE_TYPE_ASM[t.dtype]
        except KeyError as e:
            raise KeyError(f'Unknown mapping of torch dtype {t.dtype} to MLIR (possibly missing in TORCH_DTYPE_TO_IREE_TYPE_ASM table)') from e
        dim_asm = 'x'.join(['?' if d is None else str(d) for d in self.spec_dims])
        spec = f'{dim_asm}x{dtype_asm}' if dim_asm else dtype_asm
        return f'tensor<{spec}>'