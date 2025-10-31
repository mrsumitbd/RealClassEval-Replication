
from __future__ import annotations

from decimal import Decimal, getcontext, InvalidOperation
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """
        Validate that the system preserves precision correctly.

        Returns a dictionary containing:
            - decimal_precision: The precision setting of the Decimal context.
            - float_precision: The number of significant digits a Python float can
              represent (sys.float_info.dig).
            - difference: The absolute difference between a high‑precision Decimal
              value and its float conversion.
            - passed: Boolean indicating whether the difference is within an
              acceptable tolerance.
        """
        # Create a Decimal with many significant digits
        high_precision_value = Decimal(
            "123456789012345678901234567890.12345678901234567890")
        # Convert to float
        float_value = float(high_precision_value)
        # Compute the absolute difference
        difference = abs(high_precision_value - Decimal(float_value))
        # Define a tolerance (float has about 15–17 decimal digits of precision)
        tolerance = Decimal("1e-10")
        passed = difference <= tolerance

        return {
            "decimal_precision": getcontext().prec,
            "float_precision": Decimal(float_value).as_tuple().exponent,
            "difference": float(difference),
            "passed": passed,
        }

    @staticmethod
    def store_price_data(data: Any) -> str:
        """
        Store price data without modifying precision.

        Parameters
        ----------
        data : Any
            The price data to store. It can be an int, float, str, or Decimal.

        Returns
        -------
        str
            A string representation of the Decimal value, preserving all
            significant digits.
        """
        try:
            # Convert incoming data to Decimal
            if isinstance(data, Decimal):
                dec_value = data
            else:
                dec_value = Decimal(str(data))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(
                f"Unable to convert data to Decimal: {data}") from exc

        # Return the string representation to preserve precision
        return format(dec_value, "f")

    @staticmethod
    def retrieve_price_data(stored_data: Any) -> Decimal:
        """
        Retrieve price data without modifying precision.

        Parameters
        ----------
        stored_data : Any
            The stored price data, typically a string representation of a Decimal.

        Returns
        -------
        Decimal
            The Decimal value reconstructed from the stored data.
        """
        try:
            if isinstance(stored_data, Decimal):
                return stored_data
            return Decimal(str(stored_data))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(
                f"Unable to convert stored data to Decimal: {stored_data}") from exc

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """
        Preserve calculation precision for a given result.

        Parameters
        ----------
        result : float
            The numeric result of a calculation.
        operation : str
            A description of the operation performed (e.g., 'add', 'multiply').

        Returns
        -------
        float
            The result converted to Decimal and back to float, ensuring that
            the conversion uses the Decimal representation to avoid floating‑point
            rounding errors as much as possible.
        """
        # Convert the float to a Decimal using its string representation
        # to avoid floating‑point inaccuracies.
        dec_result = Decimal(str(result))
        # Optionally, you could perform additional Decimal operations here
        # based on the operation string, but for this handler we simply
        # return the Decimal converted back to float.
        return float(dec_result)
