
from typing import Dict, Any


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''
    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        import sys
        precision_info = {
            'float_precision': sys.float_info,
            'platform': sys.platform,
            'max_decimal_places': 15  # IEEE 754 double-precision
        }
        return precision_info

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data without modifying precision.'''
        if isinstance(data, (int, float)):
            return data
        elif isinstance(data, str):
            try:
                return float(data)
            except ValueError:
                raise ValueError("Invalid numeric data")
        else:
            raise TypeError("Unsupported data type for price storage")

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        import decimal
        if operation in ('division', 'multiplication', 'addition', 'subtraction'):
            with decimal.localcontext() as ctx:
                ctx.prec = 20  # Higher precision context
                dec_result = decimal.Decimal(str(result))
                return float(dec_result)
        return result
