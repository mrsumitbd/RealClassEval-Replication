
from typing import Dict, Any, Union
import decimal


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''
    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        test_value = 0.1 + 0.2
        expected_value = 0.3
        result = {
            'test_value': test_value,
            'expected_value': expected_value,
            'is_precise': test_value == expected_value
        }
        return result

    @staticmethod
    def store_price_data(data: Union[float, decimal.Decimal]) -> decimal.Decimal:
        '''Store price data using Decimal for precision.'''
        return decimal.Decimal(str(data))

    @staticmethod
    def retrieve_price_data(data: decimal.Decimal) -> decimal.Decimal:
        '''Retrieve price data without modifying precision.'''
        return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> decimal.Decimal:
        '''Preserve calculation precision using Decimal.'''
        result_decimal = decimal.Decimal(str(result))
        if operation == 'add':
            result_decimal += decimal.Decimal('0')
        elif operation == 'subtract':
            result_decimal -= decimal.Decimal('0')
        elif operation == 'multiply':
            result_decimal *= decimal.Decimal('1')
        elif operation == 'divide':
            result_decimal /= decimal.Decimal('1')
        return result_decimal
