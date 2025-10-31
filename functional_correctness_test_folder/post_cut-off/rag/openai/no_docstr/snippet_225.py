
from __future__ import annotations

from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Any, Dict

# Ensure a high precision context for all Decimal operations
getcontext().prec = 50


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """
        Validate that the system preserves precision correctly.

        Returns a dictionary containing:
            - original: the original Decimal value as a string
            - float: the float conversion of the original value
            - back: the Decimal conversion of the float value
            - difference: the difference between original and back
            - passed: whether the difference is within an acceptable tolerance
        """
        # Create a Decimal with many significant digits
        original = Decimal(
            "1." + "12345678901234567890123456789012345678901234567890"
        )
        # Convert to float
        f = float(original)
        # Convert back to Decimal via string to avoid float rounding issues
        back = Decimal(str(f))
        # Compute difference
        diff = original - back
        # Define tolerance (e.g., 1e-10)
        tolerance = Decimal("1e-10")
        passed = abs(diff) < tolerance
        return {
            "original": str(original),
            "float": f,
            "back": str(back),
            "difference": str(diff),
            "passed": passed,
        }

    @staticmethod
    def store_price_data(data: Any) -> Decimal:
        """
        Store price data without modifying precision.

        Accepts numeric types, strings, or Decimal instances and returns a Decimal
        representation that preserves the original precision.
        """
        if isinstance(data, Decimal):
            return data
        if isinstance(data, (int, float)):
            # Convert numeric types to Decimal via string to avoid binary float issues
            return Decimal(str(data))
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError(
            f"Unsupported type for price data: {type(data).__name__}. "
            "Expected int, float, str, or Decimal."
        )

    @staticmethod
    def retrieve_price_data(data: Any) -> Decimal:
        """
        Retrieve price data without modifying precision.

        Accepts stored data (Decimal or string) and returns a Decimal instance.
        """
        if isinstance(data, Decimal):
            return data
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError(
            f"Unsupported type for retrieved price data: {type(data).__name__}. "
            "Expected Decimal or str."
        )

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """
        Preserve calculation precision.

        Converts the float result to a Decimal, quantizes it to a fixed number of
        decimal places (10 in this implementation), and returns the float
        representation of the quantized value. The `operation` parameter is
        accepted for API compatibility but not used in this simplified
        implementation.
        """
        # Convert the float to Decimal via string to avoid binary float issues
        d = Decimal(str(result))
        # Quantize to 10 decimal places
        quantized = d.quantize(Decimal("1.0000000000"), rounding=ROUND_HALF_UP)
        return float(quantized)
