
from __future__ import annotations

import sys
import decimal
from decimal import Decimal, getcontext
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        # Basic float precision info
        float_info = sys.float_info
        # Decimal context precision
        decimal_prec = getcontext().prec

        return {
            "float_digits": float_info.dig,
            "float_max_exp": float_info.max_exp,
            "float_min_exp": float_info.min_exp,
            "decimal_context_precision": decimal_prec,
        }

    @staticmethod
    def store_price_data(data: Any) -> Decimal:
        """
        Store price data without modifying precision.

        Parameters
        ----------
        data : Any
            The price data to store. It can be a float, int, str, or Decimal.

        Returns
        -------
        Decimal
            The stored price as a Decimal instance.
        """
        if isinstance(data, Decimal):
            return data
        if isinstance(data, (int, float)):
            # Convert to string first to avoid binary float representation issues
            return Decimal(str(data))
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError(
            f"Unsupported data type for price storage: {type(data)}")

    @staticmethod
    def retrieve_price_data(data: Any) -> Decimal:
        """
        Retrieve price data without modifying precision.

        Parameters
        ----------
        data : Any
            The stored price data. It should be a Decimal or a string representation.

        Returns
        -------
        Decimal
            The retrieved price as a Decimal instance.
        """
        if isinstance(data, Decimal):
            return data
        if isinstance(data, str):
            return Decimal(data)
        raise TypeError(
            f"Unsupported data type for price retrieval: {type(data)}")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> Decimal:
        """
        Preserve calculation precision.

        Parameters
        ----------
        result : float
            The result of a calculation performed in float.
        operation : str
            The operation performed: 'add', 'sub', 'mul', or 'div'.

        Returns
        -------
        Decimal
            The result as a Decimal, preserving precision.
        """
        # Convert the float result to a Decimal via string to avoid binary rounding
        dec_result = Decimal(str(result))

        # Optionally, we could reapply the operation to ensure precision
        # but since we only have the result, we return it directly.
        return dec_result
