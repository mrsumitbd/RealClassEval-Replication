from typing import Any, Dict, Iterable
from decimal import Decimal, getcontext, ROUND_HALF_EVEN, InvalidOperation
import math
import copy


class PrecisionPreservingDataHandler:
    '''Handler for preserving precision in data operations.'''

    @staticmethod
    def _is_special_float(value: float) -> bool:
        return isinstance(value, float) and (math.isnan(value) or math.isinf(value))

    @staticmethod
    def _to_decimal_preserving(value: Any) -> Any:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return Decimal(value)
        if isinstance(value, float):
            if PrecisionPreservingDataHandler._is_special_float(value):
                return value
            return Decimal(str(value))
        if isinstance(value, str):
            try:
                # Attempt strict conversion from string, preserving its literal precision
                return Decimal(value)
            except (InvalidOperation, ValueError):
                return value
        if isinstance(value, dict):
            return {k: PrecisionPreservingDataHandler._to_decimal_preserving(v) for k, v in value.items()}
        if isinstance(value, list):
            return [PrecisionPreservingDataHandler._to_decimal_preserving(v) for v in value]
        if isinstance(value, tuple):
            return tuple(PrecisionPreservingDataHandler._to_decimal_preserving(v) for v in value)
        if isinstance(value, set):
            return {PrecisionPreservingDataHandler._to_decimal_preserving(v) for v in value}
        return value

    @staticmethod
    def _deep_preserving_clone(value: Any) -> Any:
        # Decimals are immutable and safe; use deepcopy for general structures
        return copy.deepcopy(value)

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        ctx = getcontext().copy()
        ctx.rounding = ROUND_HALF_EVEN

        tests = [
            ("string_exact_cents", "12.34", Decimal("12.34")),
            ("string_many_dp", "0.123456789", Decimal("0.123456789")),
            ("int_value", 123, Decimal(123)),
            ("float_short", 1.25, Decimal("1.25")),
            ("float_repeating", 0.1, Decimal("0.1")),
            ("large_price", "12345678901234567890.12",
             Decimal("12345678901234567890.12")),
        ]

        results = []
        all_pass = True

        for name, input_val, expected in tests:
            stored = PrecisionPreservingDataHandler.store_price_data(input_val)
            # Extract stored value (store returns same type or Decimal)
            stored_val = stored
            # For primitives, ensure Decimal conversion applied when appropriate
            if isinstance(input_val, (str, int, float)) and not PrecisionPreservingDataHandler._is_special_float(input_val):
                is_decimal = isinstance(stored_val, Decimal)
                equal = (stored_val == expected) if is_decimal else False
            else:
                is_decimal = isinstance(stored_val, Decimal)
                equal = True if not isinstance(
                    input_val, (str, int, float)) else is_decimal

            # Retrieve should not alter the Decimal value
            retrieved = PrecisionPreservingDataHandler.retrieve_price_data(
                stored)
            if isinstance(retrieved, Decimal) and isinstance(stored_val, Decimal):
                retrieve_equal = (retrieved == stored_val)
            else:
                retrieve_equal = retrieved == stored

            passed = bool(is_decimal and equal and retrieve_equal)
            all_pass = all_pass and passed

            results.append({
                "test": name,
                "input": str(input_val),
                "stored_type": type(stored_val).__name__,
                "stored_value": str(stored_val),
                "expected": str(expected),
                "retrieved_type": type(retrieved).__name__,
                "retrieved_value": str(retrieved),
                "passed": passed
            })

        return {
            "passed": all_pass,
            "rounding": ctx.rounding,
            "prec": ctx.prec,
            "details": results
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        return PrecisionPreservingDataHandler._to_decimal_preserving(data)

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        '''Retrieve price data without modifying precision.'''
        return PrecisionPreservingDataHandler._deep_preserving_clone(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        '''Preserve calculation precision.'''
        if isinstance(result, Decimal):
            dec = result
        else:
            if isinstance(result, float):
                if PrecisionPreservingDataHandler._is_special_float(result):
                    return result
                dec = Decimal(str(result))
            elif isinstance(result, int):
                dec = Decimal(result)
            elif isinstance(result, str):
                try:
                    dec = Decimal(result)
                except (InvalidOperation, ValueError):
                    # Fallback: attempt float parse then to Decimal
                    try:
                        f = float(result)
                        if PrecisionPreservingDataHandler._is_special_float(f):
                            return f
                        dec = Decimal(str(f))
                    except Exception:
                        raise ValueError(
                            "Unsupported result value for precision preservation")
            else:
                raise ValueError(
                    "Unsupported result value for precision preservation")

        op = (operation or "").strip().lower()

        # Determine scale by operation name hints
        if any(k in op for k in ("currency", "price", "amount")) and not any(k in op for k in ("tax", "rate", "interest", "fee")):
            scale = Decimal("0.01")
        elif any(k in op for k in ("tax", "fee", "rate", "interest")):
            scale = Decimal("0.0001")
        elif any(k in op for k in ("mul", "div", "multiply", "divide", "fx", "fxrate", "exchange")):
            scale = Decimal("0.00000001")
        else:
            scale = Decimal("0.0001")

        quantized = dec.quantize(scale, rounding=ROUND_HALF_EVEN)

        f = float(quantized)
        # Normalize negative zero
        if f == 0.0:
            f = 0.0
        return f
