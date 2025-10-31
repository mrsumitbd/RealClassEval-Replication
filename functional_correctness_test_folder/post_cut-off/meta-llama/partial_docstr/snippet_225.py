
from decimal import Decimal, getcontext
from typing import Dict, Any


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''
    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        try:
            getcontext().prec = 50
            test_value = Decimal('1.23456789012345678901234567890123456789')
            test_result = test_value + Decimal('0')
            if str(test_result) == str(test_value):
                return {'success': True, 'message': 'System precision is valid'}
            else:
                return {'success': False, 'message': 'System precision is not valid'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def store_price_data(data: Any) -> str:
        '''Store price data as a string to preserve precision.'''
        return str(data)

    @staticmethod
    def retrieve_price_data(data: str) -> Decimal:
        '''Retrieve price data without modifying precision.'''
        return Decimal(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> Decimal:
        '''Preserve calculation precision by using Decimal.'''
        getcontext().prec = 28  # Set precision according to the operation
        if operation == 'addition' or operation == 'subtraction':
            getcontext().prec = 28
        elif operation == 'multiplication':
            getcontext().prec = 56
        elif operation == 'division':
            getcontext().prec = 56
        else:
            raise ValueError('Invalid operation')

        return Decimal(str(result))
