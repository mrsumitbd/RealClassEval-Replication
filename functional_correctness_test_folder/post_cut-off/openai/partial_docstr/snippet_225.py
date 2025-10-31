
from typing import Any, Dict
import sys
import decimal
from decimal import Decimal, getcontext


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        # Check the native float precision
        float_precision = sys.float_info.mant_dig
        # Check the current Decimal context precision
        decimal_precision = getcontext().prec
        return {
            'float_precision': float_precision,
            'decimal_precision': decimal_precision,
            'float_max': sys.float_info.max,
            'float_min': sys.float_info.min,
        }

    @staticmethod
    def store_price_data(data: Any) -> Decimal:
        """
        Store price data as a Decimal to preserve precision.
        Accepts numeric types or strings that represent a number.
        """
        if isinstance(data, Decimal):
            return data
        try:
            return Decimal(str(data))
        except Exception as e:
            raise ValueError(f"Cannot convert {data!r} to Decimal: {e}")

    @staticmethod
    def retrieve_price_data(data: Any) -> Decimal:
        """
        Retrieve price data without modifying precision.
        Expects the data to be a Decimal or a value convertible to Decimal.
        """
        if isinstance(data, Decimal):
            return data
        return PrecisionPreservingDataHandler.store_price_data(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> Decimal:
        """
        Preserve calculation precision by converting the result to Decimal.
        The `operation` parameter is kept for compatibility but not used
        in this simplified implementation.
        """
        # Convert the float result to Decimal using the string representation
        # to avoid floating point inaccuracies.
        return Decimal(str(result))
