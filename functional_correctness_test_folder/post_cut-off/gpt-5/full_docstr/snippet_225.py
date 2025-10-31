from typing import Any, Dict, Union, Iterable
from decimal import Decimal, getcontext, ROUND_HALF_EVEN


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        ctx = getcontext()
        float_sum = 0.1 + 0.2
        dec_sum = Decimal('0.1') + Decimal('0.2')
        rounding_example_in = Decimal('1.005')
        rounding_example_out = rounding_example_in.quantize(
            Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        return {
            'float_imprecision': float_sum != 0.3,
            'float_sum_example': float_sum,
            'decimal_precision': dec_sum == Decimal('0.3'),
            'decimal_sum_example': str(dec_sum),
            'rounding_mode': 'ROUND_HALF_EVEN',
            'rounding_example_input': str(rounding_example_in),
            'rounding_example_output': str(rounding_example_out),
            'context_precision': ctx.prec,
            'status': 'ok'
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        def to_storable(obj: Any) -> Any:
            # Preserve None, bool, and simple immutables
            if obj is None or isinstance(obj, (bool, str)):
                return obj

            # Numbers: convert Decimal as tagged, float to Decimal via str to preserve human precision
            if isinstance(obj, Decimal):
                return {'__decimal__': format(obj, 'f')}
            if isinstance(obj, (int,)):
                return obj
            if isinstance(obj, float):
                return {'__decimal__': format(Decimal(str(obj)), 'f')}

            # Containers
            if isinstance(obj, dict):
                return {to_storable(k): to_storable(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                seq = [to_storable(x) for x in obj]
                return tuple(seq) if isinstance(obj, tuple) else seq
            if isinstance(obj, set):
                # Store sets as a tagged sorted list for deterministic output
                return {'__set__': sorted([to_storable(x) for x in obj], key=lambda x: str(x))}

            # Fallback to string representation to avoid lossy coercion
            return {'__repr__': repr(obj)}

        return to_storable(data)

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        def from_storable(obj: Any) -> Any:
            if isinstance(obj, dict):
                if '__decimal__' in obj and len(obj) == 1:
                    return Decimal(obj['__decimal__'])
                if '__set__' in obj and len(obj) == 1:
                    return set(from_storable(x) for x in obj['__set__'])
                if '__repr__' in obj and len(obj) == 1:
                    return obj['__repr__']
                return {from_storable(k): from_storable(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [from_storable(x) for x in obj]
            if isinstance(obj, tuple):
                return tuple(from_storable(x) for x in obj)
            return obj

        return from_storable(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        op = (operation or '').strip().lower()

        # Determine decimal places
        dp: Union[int, None] = None
        if op.startswith('dp:'):
            try:
                dp = int(op.split(':', 1)[1])
            except Exception:
                dp = None
        elif op in {'raw', 'none', 'no-round'}:
            dp = None
        elif op in {'price', 'amount', 'sum', 'add', 'sub', 'subtract'}:
            dp = 2
        elif op in {'percent', 'percentage', 'tax', 'interest', 'rate', 'mult', 'multiply'}:
            dp = 4
        elif op in {'fx', 'forex'}:
            dp = 6
        elif op in {'crypto'}:
            dp = 8
        else:
            dp = 2

        d = Decimal(str(result))
        if dp is None:
            return float(d)

        quant = Decimal('1').scaleb(-dp)  # 10^-dp
        rounded = d.quantize(quant, rounding=ROUND_HALF_EVEN)
        return float(rounded)
