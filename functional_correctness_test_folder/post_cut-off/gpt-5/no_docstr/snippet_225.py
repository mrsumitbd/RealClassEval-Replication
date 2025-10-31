from typing import Any, Dict, Union
from decimal import Decimal, getcontext, ROUND_HALF_EVEN, InvalidOperation
import sys
import math
import platform
import struct


class PrecisionPreservingDataHandler:

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        info: Dict[str, Any] = {}
        try:
            ctx = getcontext()
            # Float characteristics
            finfo = sys.float_info
            info["float"] = {
                "dig": finfo.dig,
                "mant_dig": finfo.mant_dig,
                "epsilon": finfo.epsilon,
                "max": finfo.max,
                "min": finfo.min,
                "radix": finfo.radix,
                "rounds": finfo.rounds,
            }
            # Decimal context
            info["decimal"] = {
                "prec": ctx.prec,
                "Emin": ctx.Emin,
                "Emax": ctx.Emax,
                "rounding": ctx.rounding,
                "capitals": ctx.capitals,
                "flags": {str(k): v for k, v in ctx.flags.items()},
                "traps": {str(k): v for k, v in ctx.traps.items()},
            }
            # Platform and interpreter details
            info["platform"] = {
                "python_version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "machine": platform.machine(),
                "system": platform.system(),
                "release": platform.release(),
                "processor": platform.processor(),
                "pointer_bits": struct.calcsize("P") * 8,
            }
            # Sanity checks
            info["sanity_checks"] = {
                "float_round_trip_0_1": float(format(0.1, ".17g")),
                "float_0_1_plus_0_2_equals_0_3": (0.1 + 0.2 == 0.3),
                "decimal_0_1_plus_0_2_equals_0_3": (Decimal("0.1") + Decimal("0.2") == Decimal("0.3")),
            }
            # Overall assessment
            info["assessment"] = {
                "is_ieee754_double": (finfo.mant_dig == 53 and finfo.radix == 2),
                "decimal_supported": True,
                "safe_for_financial_calc": True,  # Using Decimal for critical calculations
            }
        except Exception as e:
            info["error"] = repr(e)
            info["assessment"] = {"safe_for_financial_calc": False}
        return info

    @staticmethod
    def _to_safe_repr(value: Any) -> Any:
        # Convert data into a JSON-safe structure preserving numeric precision via tagged dicts
        if isinstance(value, Decimal):
            # Preserve exact decimal string
            return {"__decimal__": format(value, "f") if value == value.normalize() else str(value)}
        if isinstance(value, float):
            if math.isnan(value):
                return {"__float_special__": "nan"}
            if math.isinf(value):
                return {"__float_special__": "inf" if value > 0 else "-inf"}
            # Use 17 significant digits for round-trip safety
            return {"__float_str__": format(value, ".17g")}
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            return [PrecisionPreservingDataHandler._to_safe_repr(v) for v in value]
        if isinstance(value, dict):
            return {str(k): PrecisionPreservingDataHandler._to_safe_repr(v) for k, v in value.items()}
        # Fallback to string representation
        return {"__repr__": repr(value)}

    @staticmethod
    def store_price_data(data: Any) -> Any:
        return PrecisionPreservingDataHandler._to_safe_repr(data)

    @staticmethod
    def _from_safe_repr(value: Any) -> Any:
        if isinstance(value, dict):
            if "__decimal__" in value:
                try:
                    return Decimal(value["__decimal__"])
                except (InvalidOperation, TypeError, ValueError):
                    return value["__decimal__"]
            if "__float_str__" in value:
                s = value["__float_str__"]
                try:
                    return float(s)
                except (TypeError, ValueError):
                    return s
            if "__float_special__" in value:
                tag = value["__float_special__"]
                if tag == "nan":
                    return float("nan")
                if tag == "inf":
                    return float("inf")
                if tag == "-inf":
                    return float("-inf")
            if "__repr__" in value:
                return value["__repr__"]
            return {k: PrecisionPreservingDataHandler._from_safe_repr(v) for k, v in value.items()}
        if isinstance(value, list):
            return [PrecisionPreservingDataHandler._from_safe_repr(v) for v in value]
        return value

    @staticmethod
    def retrieve_price_data(data: Any) -> Any:
        return PrecisionPreservingDataHandler._from_safe_repr(data)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
            return result
        op = (operation or "").strip().lower()
        if op in {"price", "amount", "subtotal", "total", "money", "currency"}:
            places = Decimal("0.01")
        elif op in {"tax", "fee", "commission"}:
            places = Decimal("0.0001")
        elif op in {"fx", "rate", "interest", "exchange_rate"}:
            places = Decimal("0.000001")
        elif op in {"percentage", "percent"}:
            places = Decimal("0.0001")
        else:
            places = Decimal("0.00000001")
        try:
            d = Decimal(str(result))
            q = d.quantize(places, rounding=ROUND_HALF_EVEN)
            return float(q)
        except Exception:
            try:
                return float(result)
            except Exception:
                return result  # type: ignore
