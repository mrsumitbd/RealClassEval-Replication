
import decimal
from typing import Dict, Any


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        system_precision = {
            'float_precision': decimal.getcontext().prec,
            'decimal_precision': decimal.getcontext().prec
        }
        return system_precision

    @staticmethod
    def store_price_data(data: Any) -> Any:
        if isinstance(data, float):
            return decimal.Decimal(str(data))
        elif isinstance(data, str):
            try:
                return decimal.Decimal(data)
            except decimal.InvalidOperation:
                raise ValueError("Invalid price data format")
        else:
            raise TypeError("Unsupported data type for price data")

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        if isinstance(data, decimal.Decimal):
            return float(data)
        else:
            raise TypeError("Unsupported data type for retrieval")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        if operation == 'addition':
            return float(decimal.Decimal(str(result)))
        elif operation == 'subtraction':
            return float(decimal.Decimal(str(result)))
        elif operation == 'multiplication':
            return float(decimal.Decimal(str(result)))
        elif operation == 'division':
            return float(decimal.Decimal(str(result)))
        else:
            raise ValueError(
                "Unsupported operation for precision preservation")
