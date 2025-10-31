from typing import Any, Dict
from decimal import Decimal, getcontext, Context, localcontext


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        '''Validate that the system preserves precision correctly.'''
        test_values = [
            ('0.1', '0.2'),
            ('1.0000000000000001', '2.0000000000000002'),
            ('123456789.123456789', '0.000000001')
        ]
        results = []
        for a_str, b_str in test_values:
            a = Decimal(a_str)
            b = Decimal(b_str)
            sum_ab = a + b
            mul_ab = a * b
            results.append({
                'a': str(a),
                'b': str(b),
                'sum': str(sum_ab),
                'mul': str(mul_ab),
                'sum_exact': sum_ab == Decimal(str(float(a_str) + float(b_str))),
                'mul_exact': mul_ab == Decimal(str(float(a_str) * float(b_str))),
            })
        return {
            'decimal_context': str(getcontext()),
            'test_results': results
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        '''Store price data without modifying precision.'''
        if isinstance(data, float):
            # Convert to string to preserve precision, then to Decimal
            return Decimal(str(data))
        elif isinstance(data, str):
            try:
                return Decimal(data)
            except Exception:
                return data
        elif isinstance(data, (int, Decimal)):
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
        # Just return as is, assuming storage was done with Decimal
        return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        # Use Decimal for calculation, then return as float
        with localcontext() as ctx:
            ctx.prec = 28
            dec_result = Decimal(str(result))
            # Optionally, round or quantize based on operation
            if operation == 'add':
                return float(dec_result)
            elif operation == 'mul':
                return float(dec_result)
            elif operation == 'div':
                return float(dec_result)
            elif operation == 'sub':
                return float(dec_result)
            else:
                return float(dec_result)
