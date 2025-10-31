
import sys
import math
from typing import Dict, Any


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        precision_info = {
            'float_precision': sys.float_info,
            'max_float': sys.float_info.max,
            'min_float': sys.float_info.min,
            'epsilon': sys.float_info.epsilon
        }
        return precision_info

    @staticmethod
    def store_price_data(data: Any) -> Any:
        if isinstance(data, (int, float)):
            return float(data)
        elif isinstance(data, str):
            try:
                return float(data)
            except ValueError:
                raise ValueError("Cannot convert string to float")
        else:
            raise TypeError("Unsupported data type for price storage")

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        if isinstance(data, (int, float)):
            return float(data)
        elif isinstance(data, str):
            try:
                return float(data)
            except ValueError:
                raise ValueError("Cannot convert string to float")
        else:
            raise TypeError("Unsupported data type for price retrieval")

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        if operation == 'add':
            return math.fsum([result])
        elif operation == 'multiply':
            return math.exp(math.log(result)) if result > 0 else result
        elif operation == 'divide':
            return result if result != 0 else 0.0
        else:
            return float(result)
