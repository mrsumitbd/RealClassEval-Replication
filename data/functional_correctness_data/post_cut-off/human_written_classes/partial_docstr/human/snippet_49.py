import torch

class PrecisionType:
    """Type of precision used."""

    @staticmethod
    def is_fp16(precision: str) -> bool:
        return precision in HALF_LIST

    @staticmethod
    def is_fp32(precision: str) -> bool:
        return precision in FLOAT_LIST

    @staticmethod
    def is_bf16(precision: str) -> bool:
        return precision in BFLOAT_LIST

    @staticmethod
    def to_dtype(precision: str) -> torch.dtype:
        if precision in HALF_LIST:
            return torch.float16
        elif precision in FLOAT_LIST:
            return torch.float32
        elif precision in BFLOAT_LIST:
            return torch.bfloat16
        else:
            raise RuntimeError(f'Unexpected precision: {precision}')

    @staticmethod
    def to_str(precision: torch.dtype) -> str:
        if precision == torch.float16:
            return 'float16'
        elif precision == torch.float32:
            return 'float32'
        elif precision == torch.bfloat16:
            return 'bfloat16'
        else:
            raise RuntimeError(f'Unexpected precision: {precision}')