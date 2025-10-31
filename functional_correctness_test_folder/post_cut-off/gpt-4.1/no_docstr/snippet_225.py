
from typing import Dict, Any
import sys
import decimal
import json


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        float_info = sys.float_info
        decimal_context = decimal.getcontext()
        return {
            "float_max": float_info.max,
            "float_epsilon": float_info.epsilon,
            "float_digits": float_info.dig,
            "decimal_prec": decimal_context.prec,
            "decimal_Emax": decimal_context.Emax,
            "decimal_Emin": decimal_context.Emin
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        # Store price data as stringified Decimal for precision
        if isinstance(data, float):
            dec = decimal.Decimal(str(data))
            return str(dec)
        elif isinstance(data, decimal.Decimal):
            return str(data)
        elif isinstance(data, dict):
            # Recursively store all float/Decimal values as strings
            def convert(v):
                if isinstance(v, float):
                    return str(decimal.Decimal(str(v)))
                elif isinstance(v, decimal.Decimal):
                    return str(v)
                elif isinstance(v, dict):
                    return {k: convert(val) for k, val in v.items()}
                elif isinstance(v, list):
                    return [convert(i) for i in v]
                else:
                    return v
            return json.dumps(convert(data))
        else:
            return str(data)

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        # Retrieve price data as Decimal from string
        if isinstance(data, str):
            try:
                # Try to load as JSON
                loaded = json.loads(data)

                def convert_back(v):
                    if isinstance(v, str):
                        try:
                            return decimal.Decimal(v)
                        except Exception:
                            return v
                    elif isinstance(v, dict):
                        return {k: convert_back(val) for k, val in v.items()}
                    elif isinstance(v, list):
                        return [convert_back(i) for i in v]
                    else:
                        return v
                return convert_back(loaded)
            except Exception:
                # Not JSON, try Decimal
                try:
                    return decimal.Decimal(data)
                except Exception:
                    return data
        else:
            return data

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        # Use Decimal for calculation, then return as float
        d_result = decimal.Decimal(str(result))
        if operation == "round":
            # Round to 8 decimal places (typical for prices)
            d_result = d_result.quantize(decimal.Decimal(
                '0.00000001'), rounding=decimal.ROUND_HALF_UP)
        elif operation == "floor":
            d_result = d_result.to_integral_value(rounding=decimal.ROUND_FLOOR)
        elif operation == "ceil":
            d_result = d_result.to_integral_value(
                rounding=decimal.ROUND_CEILING)
        # Add more operations as needed
        return float(d_result)
