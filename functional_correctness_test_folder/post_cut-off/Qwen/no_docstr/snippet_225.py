
from typing import Dict, Any, Union
import decimal


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        return {
            "system_precision": decimal.getcontext().prec,
            "system_rounding": decimal.getcontext().rounding
        }

    @staticmethod
    def store_price_data(data: Union[float, decimal.Decimal]) -> decimal.Decimal:
        return decimal.Decimal(str(data))

    @staticmethod
    def retrieve_price_data(data: decimal.Decimal) -> float:
        return float(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> decimal.Decimal:
        result_decimal = decimal.Decimal(str(result))
        if operation in ["add", "subtract", "multiply", "divide"]:
            decimal.getcontext().prec = max(decimal.getcontext().prec, len(str(result_decimal)))
        return result_decimal
