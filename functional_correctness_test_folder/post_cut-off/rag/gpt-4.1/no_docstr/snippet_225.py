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
            'decimal_context_prec': context.prec,
            'test_value': str(test_value),
            'expected': str(expected),
            'is_precise': is_precise
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data without modifying precision.'''
        if isinstance(data, float):
            # Convert to string then Decimal to avoid float imprecision
            return Decimal(str(data))
        elif isinstance(data, (int, Decimal)):
            return Decimal(data)
        elif isinstance(data, str):
            return Decimal(data)
        elif isinstance(data, list):
            return [PrecisionPreservingDataHandler.store_price_data(d) for d in data]
        elif isinstance(data, dict):
            return {k: PrecisionPreservingDataHandler.store_price_data(v) for k, v in data.items()}
        else:
            return data

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        # For this handler, just return the data as is (assumed to be Decimal or original type)
        return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        # Use Decimal for calculation, then return as float
        d_result = Decimal(str(result))
        if operation == 'round':
            # Round to 2 decimal places using banker's rounding
            d_result = d_result.quantize(
                Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        elif operation == 'floor':
            d_result = d_result.to_integral_value(rounding='ROUND_FLOOR')
        elif operation == 'ceil':
            d_result = d_result.to_integral_value(rounding='ROUND_CEILING')
        # Add more operations as needed
        return float(d_result)
