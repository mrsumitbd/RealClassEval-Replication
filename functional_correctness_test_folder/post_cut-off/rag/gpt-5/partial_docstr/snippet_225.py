from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        ctx = getcontext()

        decimal_sum = Decimal('0.1') + Decimal('0.2')
        float_sum = 0.1 + 0.2

        price_str = '12.3400'
        stored = PrecisionPreservingDataHandler.store_price_data(price_str)
        retrieved = PrecisionPreservingDataHandler.retrieve_price_data(stored)
        trailing_zeros_preserved = isinstance(
            retrieved, Decimal) and str(retrieved) == price_str

        return {
            'decimal_context_precision': ctx.prec,
            'decimal_context_rounding': ctx.rounding,
            'decimal_addition_exact': decimal_sum == Decimal('0.3'),
            'float_addition_exact': float_sum == 0.3,
            'trailing_zeros_preserved': trailing_zeros_preserved,
            'stored_representation_type': type(stored).__name__,
            'retrieved_type': type(retrieved).__name__,
            'sample_values': {
                'decimal_sum': str(decimal_sum),
                'float_sum': repr(float_sum),
            },
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        """Store price data without modifying precision."""
        if isinstance(data, Decimal):
            return str(data)
        if isinstance(data, str):
            # Validate numeric form without altering representation.
            Decimal(data)  # may raise InvalidOperation
            return data
        if isinstance(data, int):
            return str(data)
        if isinstance(data, float):
            raise TypeError(
                'Float input is not supported for precise price storage. Use str or Decimal.')
        raise TypeError(
            f'Unsupported data type for storage: {type(data).__name__}')

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        """Retrieve price data without modifying precision."""
        if isinstance(data, Decimal):
            return data
        if isinstance(data, str):
            return Decimal(data)
        if isinstance(data, int):
            return Decimal(data)
        if isinstance(data, float):
            raise TypeError(
                'Float input is not supported for precise price retrieval. Use str or Decimal.')
        raise TypeError(
            f'Unsupported data type for retrieval: {type(data).__name__}')

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """Preserve calculation precision."""
        op = (operation or '').lower()
        if op in ('add', 'sum', 'subtract', 'sub', 'plus', 'minus'):
            quant = Decimal('0.01')
        elif op in ('multiply', 'mul', 'times', 'divide', 'div'):
            quant = Decimal('0.0001')
        else:
            quant = Decimal('0.01')

        dec_result = Decimal(str(result))
        quantized = dec_result.quantize(quant, rounding=ROUND_HALF_EVEN)
        return float(quantized)
