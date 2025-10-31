from decimal import Decimal, getcontext, localcontext, ROUND_HALF_EVEN, InvalidOperation
from typing import Any, Dict, Mapping, Sequence


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        ctx = getcontext()
        float_sum = 0.1 + 0.2
        decimal_sum = Decimal("0.1") + Decimal("0.2")

        results: Dict[str, Any] = {
            "decimal_context": {
                "prec": ctx.prec,
                "rounding": ctx.rounding,
                "Emax": ctx.Emax,
                "Emin": ctx.Emin,
                "capitals": ctx.capitals,
                "clamp": ctx.clamp,
            },
            "float_sum_test": {
                "0.1+0.2": float_sum,
                "equals_0.3": float_sum == 0.3,
                "difference_from_0.3": float_sum - 0.3,
            },
            "decimal_sum_test": {
                "0.1+0.2": str(decimal_sum),
                "equals_0.3": decimal_sum == Decimal("0.3"),
            },
        }

        # Demonstrate exact preservation from floats vs. decimal strings
        df_01 = Decimal.from_float(0.1)
        df_02 = Decimal.from_float(0.2)
        df_03 = Decimal.from_float(0.3)
        df_sum = df_01 + df_02

        results["decimal_from_float_test"] = {
            "0.1_from_float": str(df_01),
            "0.2_from_float": str(df_02),
            "0.3_from_float": str(df_03),
            "sum_from_float": str(df_sum),
            "sum_equals_0.3_from_float": df_sum == df_03,
            "sum_equals_decimal_0.3": df_sum == Decimal("0.3"),
        }

        # Demonstrate banker’s rounding behavior
        with localcontext() as lctx:
            lctx.rounding = ROUND_HALF_EVEN
            r1 = Decimal("1.005").quantize(
                Decimal("0.01"), rounding=ROUND_HALF_EVEN)
            r2 = Decimal("1.015").quantize(
                Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        results["round_half_even_test"] = {
            "1.005_to_2dp": str(r1),
            "1.015_to_2dp": str(r2),
        }

        results["status"] = "ok" if (results["decimal_sum_test"]["equals_0.3"]
                                     and not results["float_sum_test"]["equals_0.3"]) else "check"
        return results

    @staticmethod
    def store_price_data(data: Any) -> Any:
        """Store price data without modifying precision."""
        def to_decimal(value: Any) -> Any:
            if isinstance(value, Decimal):
                return value
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                return Decimal(value)
            if isinstance(value, float):
                return Decimal.from_float(value)
            if isinstance(value, str):
                try:
                    return Decimal(value)
                except Exception:
                    return value
            if isinstance(value, Mapping):
                return {k: to_decimal(v) for k, v in value.items()}
            if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
                typ = type(value)
                converted = [to_decimal(v) for v in value]
                return typ(converted) if typ in (list, tuple) else converted
            return value

        return to_decimal(data)

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        """Retrieve price data without modifying precision."""
        def from_storage(value: Any) -> Any:
            # Keep Decimals as-is, convert numeric-like strings to Decimal, avoid floats
            if isinstance(value, Decimal):
                return value
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                return Decimal(value)
            if isinstance(value, float):
                return Decimal.from_float(value)
            if isinstance(value, str):
                try:
                    return Decimal(value)
                except Exception:
                    return value
            if isinstance(value, Mapping):
                return {k: from_storage(v) for k, v in value.items()}
            if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
                typ = type(value)
                converted = [from_storage(v) for v in value]
                return typ(converted) if typ in (list, tuple) else converted
            return value

        return from_storage(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """Preserve calculation precision."""
        try:
            d = Decimal.from_float(result)
        except Exception:
            try:
                d = Decimal(str(result))
            except Exception:
                return result

        # Choose scale based on operation; defaults to cents
        op = (operation or "").strip().lower()
        if op in {"div", "divide", "ratio", "rate"}:
            scale = Decimal("0.0001")
        elif op in {"tax", "interest", "fx", "fx_rate", "fee"}:
            scale = Decimal("0.0001")
        elif op in {"mul", "multiply", "product"}:
            scale = Decimal("0.01")
        elif op in {"add", "sum", "sub", "subtract"}:
            scale = Decimal("0.01")
        else:
            scale = Decimal("0.01")

        with localcontext() as lctx:
            lctx.rounding = ROUND_HALF_EVEN
            try:
                quantized = d.quantize(scale, rounding=ROUND_HALF_EVEN)
            except (InvalidOperation, ValueError):
                return float(d)
        return float(quantized)
