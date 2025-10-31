from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation
from typing import Any, Dict, Mapping, Iterable


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        float_sum = 0.1 + 0.2
        dec_sum = Decimal("0.1") + Decimal("0.2")
        third = (Decimal("1") / Decimal("3")
                 ).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

        decimal_precision_ok = (
            dec_sum == Decimal("0.3")
            and third == Decimal("0.33")
        )

        return {
            "float_precision_issue_demo": {
                "0.1+0.2": float_sum,
                "equals_0.3": float_sum == 0.3,
            },
            "decimal_precision_demo": {
                "0.1+0.2": str(dec_sum),
                "equals_0.3": dec_sum == Decimal("0.3"),
            },
            "quantize_demo": str(third),
            "decimal_precision_ok": decimal_precision_ok,
            "status": "ok" if decimal_precision_ok else "error",
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        """Store price data without modifying precision."""
        return PrecisionPreservingDataHandler._to_precise(data)

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        """Retrieve price data without modifying precision."""
        # Returning as precise representations; if already precise, unchanged.
        return PrecisionPreservingDataHandler._to_precise(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """Preserve calculation precision."""
        # Map common operation types to appropriate quantization scales.
        scale_map: Dict[str, str] = {
            "price": "0.01",
            "currency": "0.01",
            "tax": "0.01",
            "discount": "0.01",
            "percentage": "0.0001",
            "rate": "0.000001",
            "interest": "0.000001",
            "default": "0.0000000001",
        }

        try:
            dec = Decimal(str(result))
        except Exception:
            return result

        if not dec.is_finite():
            return float(result)

        quant = Decimal(scale_map.get(operation.lower(), scale_map["default"]))
        try:
            precise = dec.quantize(quant, rounding=ROUND_HALF_EVEN)
        except (InvalidOperation, ValueError):
            precise = dec

        try:
            return float(precise)
        except (OverflowError, ValueError):
            # As a last resort, return the original float
            return result

    @staticmethod
    def _to_precise(value: Any) -> Any:
        """Convert numeric-like values to precise Decimal representations recursively."""
        # Preserve Decimal as-is
        if isinstance(value, Decimal):
            return value

        # Convert floats through string to keep intended human-readable digits
        if isinstance(value, float):
            try:
                return Decimal(str(value))
            except Exception:
                return value

        # Integers convert exactly to Decimal
        if isinstance(value, int):
            return Decimal(value)

        # For strings, try to interpret as Decimal; otherwise leave unchanged
        if isinstance(value, str):
            try:
                d = Decimal(value)
                return d
            except Exception:
                return value

        # For mappings, recursively convert values
        if isinstance(value, Mapping):
            try:
                return type(value)(
                    (k, PrecisionPreservingDataHandler._to_precise(v)) for k, v in value.items()
                )
            except Exception:
                return {k: PrecisionPreservingDataHandler._to_precise(v) for k, v in value.items()}

        # For iterable containers (list, tuple, set), recursively convert items
        if isinstance(value, (list, tuple, set)):
            converted = [
                PrecisionPreservingDataHandler._to_precise(v) for v in value]
            if isinstance(value, tuple):
                return tuple(converted)
            if isinstance(value, set):
                # Sets may lose ordering; keep type but ensure hashability
                try:
                    return type(value)(converted)
                except TypeError:
                    return set(converted)
            return converted

        # For other types, return unchanged
        return value
