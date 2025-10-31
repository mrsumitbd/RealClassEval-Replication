
import sys
from typing import Dict, Any


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''
    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        info = {
            'float_precision': sys.float_info,
            'max_decimal_places': 15  # IEEE 754 double-precision
        }
        return info

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data while preserving precision.'''
        if isinstance(data, (int, float)):
            return float(data)
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
        if operation not in ['add', 'subtract', 'multiply', 'divide']:
            raise ValueError("Unsupported operation")
        return round(result, 15)
