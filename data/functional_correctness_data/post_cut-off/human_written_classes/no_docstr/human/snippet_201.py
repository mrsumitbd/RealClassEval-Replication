from dataclasses import dataclass

@dataclass
class Kernel:
    sm: int
    dtype: str
    dtype_out: str
    head_dim: int
    softcap: bool
    direction: str
    disable_fwd_atomic_reduction: bool = False
    disable_bwd_dkv_atomic_reduction: bool = False

    @property
    def template(self) -> str:
        if self.direction == 'fwd':
            if self.sm == 90:
                return KERNEL_IMPL_TEMPLATE_FWD_SM90.format(ARCH=str(self.sm), DTYPE=DTYPE_MAP[self.dtype], DTYPE_OUT=DTYPE_OUT_MAP[self.dtype_out], HEAD_DIM=self.head_dim, SOFTCAP=str(self.softcap).lower(), DISABLE_FWD_ATOMIC_REDUCTION=str(self.disable_fwd_atomic_reduction).lower())
            else:
                raise NotImplementedError('Support for SM versions other than 90 is not implemented yet.')
        elif self.direction == 'bwd':
            if self.sm == 90:
                return KERNEL_IMPL_TEMPLATE_BWD_SM90.format(ARCH=str(self.sm), DTYPE=DTYPE_MAP[self.dtype], DTYPE_OUT=DTYPE_OUT_MAP[self.dtype_out], HEAD_DIM=self.head_dim, SOFTCAP=str(self.softcap).lower(), DISABLE_BWD_DKV_ATOMIC_REDUCTION=str(self.disable_bwd_dkv_atomic_reduction).lower())
            else:
                raise NotImplementedError('Support for SM versions other than 90 is not implemented yet.')
        else:
            raise ValueError(f'Unknown direction: {self.direction}')

    @property
    def filename(self) -> str:
        return f"flash_{self.direction}_hdim{self.head_dim}_{self.dtype}_{self.dtype_out}{('_softcap' if self.softcap else '')}{('_disable_fwd_atomic_reduction' if self.disable_fwd_atomic_reduction else '')}{('_disable_bwd_dkv_atomic_reduction' if self.disable_bwd_dkv_atomic_reduction else '')}_sm{self.sm}.cu"