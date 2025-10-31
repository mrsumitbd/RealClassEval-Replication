
from typing import Dict, Any
import sys
import decimal
import math


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        float_epsilon = sys.float_info.epsilon
        decimal_prec = decimal.getcontext().prec
        # Test float precision
        float_test = 0.1 + 0.2
        float_expected = 0.3
        float_ok = math.isclose(float_test, float_expected, rel_tol=1e-9)
        # Test decimal precision
        d1 = decimal.Decimal('0.1')
        d2 = decimal.Decimal('0.2')
        d_sum = d1 + d2
        decimal_ok = (d_sum == decimal.Decimal('0.3'))
        return {
            'float_epsilon': float_epsilon,
            'decimal_precision': decimal_prec,
            'float_precision_ok': float_ok,
            'decimal_precision_ok': decimal_ok
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''
        Store price data as string to preserve precision.
        Accepts float, Decimal, or string.
        '''
        if isinstance(data, decimal.Decimal):
            return str(data)
        elif isinstance(data, float):
            # Use repr to preserve as much precision as possible
            return repr(data)
        elif isinstance(data, str):
            # Assume already stringified
            return data
        else:
            raise TypeError("Unsupported data type for storing price data.")

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        # Try to return as Decimal if possible
        if isinstance(data, decimal.Decimal):
            return data
        elif isinstance(data, str):
            try:
                return decimal.Decimal(data)
            except decimal.InvalidOperation:
                raise ValueError("String data cannot be converted to Decimal.")
        elif isinstance(data, float):
            # Convert float to Decimal using str to avoid float imprecision
            return decimal.Decimal(str(data))
        else:
            raise TypeError("Unsupported data type for retrieving price data.")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        # For certain operations, round to a reasonable number of decimal places
        # For price, typically 2-8 decimals are used
        if operation in ('add', 'sub', 'mul', 'div'):
            # Use decimal for precision, then convert back to float
            d_result = decimal.Decimal(str(result))
            # Let's assume 8 decimal places for price calculations
            d_result = d_result.quantize(decimal.Decimal('0.00000001'))
            return float(d_result)
        else:
            # For unknown operations, just return as is
            return result
