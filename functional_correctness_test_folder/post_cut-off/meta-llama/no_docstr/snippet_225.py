
from decimal import Decimal, getcontext
from typing import Dict, Any


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """Validate the system's precision for decimal operations."""
        precision_status = {
            'precision': getcontext().prec,
            'rounding_mode': getcontext().rounding,
            # Assuming a minimum precision of 28 is required
            'is_valid': getcontext().prec >= 28
        }
        return precision_status

    @staticmethod
    def store_price_data(data: Any) -> str:
        """Store price data as a string to preserve precision."""
        if isinstance(data, (int, float)):
            return str(Decimal(str(data)))
        elif isinstance(data, str):
            try:
                # Validate if the string can be converted to Decimal
                Decimal(data)
                return data
            except Exception as e:
                raise ValueError("Invalid price data") from e
        else:
            raise TypeError("Unsupported data type for price data")

    @staticmethod
    def retrieve_price_data(data: str) -> Decimal:
        """Retrieve price data as a Decimal object."""
        try:
            return Decimal(data)
        except Exception as e:
            raise ValueError("Invalid stored price data") from e

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """Preserve precision during calculations by using Decimal."""
        try:
            decimal_result = Decimal(str(result))
            if operation == 'addition' or operation == 'subtraction':
                getcontext().prec = max(getcontext().prec, len(str(result)) + 2)
            elif operation == 'multiplication':
                getcontext().prec = max(getcontext().prec, len(str(result)) * 2)
            elif operation == 'division':
                getcontext().prec = max(getcontext().prec, len(
                    str(result)) + 10)  # Increase precision for division
            else:
                raise ValueError("Unsupported operation")
            return float(decimal_result)
        except Exception as e:
            raise ValueError("Failed to preserve calculation precision") from e
