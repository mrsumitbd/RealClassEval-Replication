from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        # Set a high precision context for the test
        getcontext().prec = 50
        # Create a Decimal with many digits
        original = Decimal(
            "12345678901234567890123456789012345678901234567890.123456789012345678901234567890"
        )
        # Convert to float (lossy)
        float_value = float(original)
        # Convert back to Decimal for comparison
        reconverted = Decimal(str(float_value))
        # Compute difference
        difference = original - reconverted
        passed = difference == Decimal(0)
        return {
            "original": str(original),
            "float_value": float_value,
            "reconverted": str(reconverted),
            "difference": str(difference),
            "passed": passed,
        }

    @staticmethod
    def store_price_data(data: Any) -> Decimal:
        """Store price data without modifying precision."""
        if isinstance(data, Decimal):
            return data
        if isinstance(data, (int, float)):
            return Decimal(str(data))
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError("Unsupported data type for price storage")

    @staticmethod
    def retrieve_price_data(data: Any) -> Decimal:
        """Retrieve price data without modifying precision."""
        if isinstance(data, Decimal):
            return data
        if isinstance(data, (int, float)):
            return Decimal(str(data))
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError("Unsupported data type for price retrieval")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> Decimal:
        """Preserve calculation precision."""
        # Convert the float result to Decimal using its string representation
        result_decimal = Decimal(str(result))
        # Perform the requested operation using Decimal arithmetic
        if operation == "sqrt":
            # Use the context's precision for sqrt
            return result_decimal.sqrt()
        elif operation == "round":
            # Round to the same number of decimal places as the original string
            return result_decimal.quantize(Decimal("1." + "0" * len(result_decimal.as_tuple().exponent * -1)))
        # Default: return the Decimal representation
        return result_decimal
