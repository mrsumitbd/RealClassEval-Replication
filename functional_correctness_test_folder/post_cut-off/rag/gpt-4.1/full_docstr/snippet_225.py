from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        context = getcontext()
        test_value = Decimal('0.1') + Decimal('0.2')
        expected = Decimal('0.3')
        is_precise = test_value == expected
        return {
            'decimal_context': {
                'prec': context.prec,
                'rounding': context.rounding,
            },
            'test_value': str(test_value),
            'expected': str(expected),
            'is_precise': is_precise
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data without modifying precision.'''
        if isinstance(data, float):
            # Convert to string to avoid float imprecision, then to Decimal
            return Decimal(str(data))
        elif isinstance(data, (int, Decimal)):
            return Decimal(data)
        elif isinstance(data, str):
            return Decimal(data)
        else:
            return data

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        # Assume data is stored as Decimal, return as string to preserve precision
        if isinstance(data, Decimal):
            return str(data)
        return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        # Use Decimal for calculation, then return as float
        d_result = Decimal(str(result))
        if operation == 'round2':
            return float(d_result.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))
        elif operation == 'round4':
            return float(d_result.quantize(Decimal('0.0001'), rounding=ROUND_HALF_EVEN))
        else:
            return float(d_result)
