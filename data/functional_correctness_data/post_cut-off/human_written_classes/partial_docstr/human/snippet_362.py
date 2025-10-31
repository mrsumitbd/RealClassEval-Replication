import torch
from typing import Union

class PrecisionType:
    """Type of precision used.

    >>> PrecisionType.HALF == 16
    True
    >>> PrecisionType.HALF in (16, "16")
    True
    """
    HALF = '16'
    FLOAT = '32'
    FULL = '64'
    BFLOAT = 'bf16'
    MIXED = 'mixed'

    @staticmethod
    def supported_type(precision: Union[str, int]) -> bool:
        return any((x == precision for x in PrecisionType))

    @staticmethod
    def supported_types() -> list[str]:
        return [x.value for x in PrecisionType]

    @staticmethod
    def is_fp16(precision):
        return precision in HALF_LIST

    @staticmethod
    def is_fp32(precision):
        return precision in FLOAT_LIST

    @staticmethod
    def is_bf16(precision):
        return precision in BFLOAT_LIST

    @staticmethod
    def to_dtype(precision):
        if precision in HALF_LIST:
            return torch.float16
        elif precision in FLOAT_LIST:
            return torch.float32
        elif precision in BFLOAT_LIST:
            return torch.bfloat16
        else:
            raise RuntimeError(f'unexpected precision: {precision}')

    @staticmethod
    def to_str(precision):
        if precision == torch.float16:
            return 'fp16'
        elif precision == torch.float32:
            return 'fp32'
        elif precision == torch.bfloat16:
            return 'bf16'
        else:
            raise RuntimeError(f'unexpected precision: {precision}')