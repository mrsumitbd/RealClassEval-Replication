
from decimal import Decimal, getcontext
from typing import Any, Dict


class PrecisionPreservingDataHandler:
    """Handler for preserving precision in data operations."""

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate that the system preserves precision correctly."""
        getcontext().prec = 28  # Set the precision to 28 decimal places
        test_decimal = Decimal('1.2345678901234567890123456789')
        test_result = test_decimal * Decimal('1')
        return {
            'precision': getcontext().prec,
            'test_result': str(test_result),
            'is_precise': str(test_result) == str(test_decimal)
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        """Store price data without modifying precision."""
        if isinstance(data, float):
            return str(Decimal(str(data)))
        elif isinstance(data, str):
            try:
                Decimal(data)
                return data
            except Exception as e:
                raise ValueError("Invalid price data") from e
        else:
            raise TypeError("Unsupported data type for price data")

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        """Retrieve price data without modifying precision."""
        if isinstance(data, str):
            return Decimal(data)
        else:
            raise TypeError("Unsupported data type for price data")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """Preserve calculation precision."""
        getcontext().prec = 28
        decimal_result = Decimal(str(result))
        return float(decimal_result)
