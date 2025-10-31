
from typing import Dict, Any
import sys
import decimal


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        float_info = sys.float_info
        decimal_context = decimal.getcontext()
        test_float = 0.1 + 0.2
        test_decimal = decimal.Decimal('0.1') + decimal.Decimal('0.2')
        return {
            'float_epsilon': float_info.epsilon,
            'float_max': float_info.max,
            'float_min': float_info.min,
            'decimal_prec': decimal_context.prec,
            'decimal_epsilon': decimal.Decimal(1).next_minus() - decimal.Decimal(1),
            'test_float_0.1+0.2': test_float,
            'test_decimal_0.1+0.2': str(test_decimal),
            'float_vs_decimal_equal': abs(test_float - float(test_decimal)) < float_info.epsilon
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data without modifying precision.'''
        # If data is float, convert to Decimal for storage
        if isinstance(data, float):
            return decimal.Decimal(str(data))
        elif isinstance(data, (int, decimal.Decimal, str)):
            return data
        elif isinstance(data, list):
            return [PrecisionPreservingDataHandler.store_price_data(d) for d in data]
        elif isinstance(data, dict):
            return {k: PrecisionPreservingDataHandler.store_price_data(v) for k, v in data.items()}
        else:
            return data

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        # Return as is, but if Decimal, convert to float for use
        if isinstance(data, decimal.Decimal):
            return float(data)
        elif isinstance(data, (int, float, str)):
            return data
        elif isinstance(data, list):
            return [PrecisionPreservingDataHandler.retrieve_price_data(d) for d in data]
        elif isinstance(data, dict):
            return {k: PrecisionPreservingDataHandler.retrieve_price_data(v) for k, v in data.items()}
        else:
            return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        # Use decimal for critical operations
        if operation in {'add', 'sub', 'mul', 'div'}:
            d_result = decimal.Decimal(str(result))
            return float(+d_result)  # unary plus applies context precision
        else:
            return result
