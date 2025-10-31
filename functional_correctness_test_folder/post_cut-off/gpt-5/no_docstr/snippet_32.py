from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

# Assuming these types are provided by the surrounding codebase
# from .pricing import PricingCalculator, CostMode
# from .timezones import TimezoneHandler
# from .models import UsageEntry


class UsageEntryMapper:

    def __init__(self, pricing_calculator: "PricingCalculator", timezone_handler: "TimezoneHandler"):
        self._pricing_calculator = pricing_calculator
        self._timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: "CostMode") -> Optional["UsageEntry"]:
        if not isinstance(data, dict) or not data:
            return None

        tokens = self._extract_tokens(data)
        if not self._has_valid_tokens(tokens):
            return None

        ts = self._extract_timestamp(data)
        if ts is None:
            return None

        model = self._extract_model(data)
        if not model:
            return None

        metadata = self._extract_metadata(data)
        cost = self._calculate_cost_safe(model, tokens, mode)

        entry = self._build_usage_entry_safe(
            timestamp=ts,
            model=model,
            tokens=tokens,
            cost=cost,
            mode=mode,
            metadata=metadata,
        )
        return entry

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        if not isinstance(tokens, dict):
            return False
        for k in ("prompt", "completion", "total"):
            v = tokens.get(k)
            if isinstance(v, int) and v > 0:
                return True
        return False

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        candidates = [
            data.get("timestamp"),
            data.get("time"),
            data.get("created_at"),
            data.get("created"),
            data.get("ts"),
        ]
        value = next((c for c in candidates if c is not None), None)
        if value is None:
            return None

        # Delegate to timezone handler if it provides parsing
        handler = self._timezone_handler
        try:
            if hasattr(handler, "parse"):
                dt = handler.parse(value)  # type: ignore[attr-defined]
                if isinstance(dt, datetime):
                    return dt
            if hasattr(handler, "parse_to_utc"):
                dt = handler.parse_to_utc(value)  # type: ignore[attr-defined]
                if isinstance(dt, datetime):
                    return dt
            if hasattr(handler, "to_datetime"):
                dt = handler.to_datetime(value)  # type: ignore[attr-defined]
                if isinstance(dt, datetime):
                    return self._ensure_utc(dt)
        except Exception:
            pass

        # Fallback parsing
        try:
            if isinstance(value, (int, float)):
                # Heuristic: treat large numbers as ms
                ts_val = float(value)
                if ts_val > 1e12:
                    dt = datetime.fromtimestamp(
                        ts_val / 1000.0, tz=timezone.utc)
                elif ts_val > 1e10:
                    dt = datetime.fromtimestamp(
                        ts_val / 1000.0, tz=timezone.utc)
                else:
                    dt = datetime.fromtimestamp(ts_val, tz=timezone.utc)
                return dt
            if isinstance(value, str):
                for fmt in (
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S%z",
                    "%Y-%m-%d %H:%M:%S",
                ):
                    try:
                        dt = datetime.strptime(value, fmt)
                        return self._ensure_utc(dt)
                    except Exception:
                        continue
                # Last resort: fromisoformat
                try:
                    dt = datetime.fromisoformat(value)
                    return self._ensure_utc(dt)
                except Exception:
                    pass
        except Exception:
            return None

        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        for key in ("model", "model_name", "gpt_model", "engine", "deployment", "deployment_name"):
            v = data.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        # Nested places commonly used
        usage = data.get("usage") if isinstance(
            data.get("usage"), dict) else None
        if usage:
            for key in ("model", "model_name"):
                v = usage.get(key)
                if isinstance(v, str) and v.strip():
                    return v.strip()
        return ""

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        result: Dict[str, str] = {}

        md = data.get("metadata")
        if isinstance(md, dict):
            for k, v in md.items():
                try:
                    result[str(k)] = self._to_str(v)
                except Exception:
                    continue

        # Common auxiliary fields
        for key in ("user_id", "user", "request_id", "id", "source", "project", "organization", "org_id"):
            v = data.get(key)
            if v is not None and str(key) not in result:
                try:
                    result[str(key)] = self._to_str(v)
                except Exception:
                    pass

        return result

    def _extract_tokens(self, data: Dict[str, Any]) -> Dict[str, int]:
        tokens: Dict[str, int] = {"prompt": 0, "completion": 0, "total": 0}

        def assign_if_int(target: str, value: Any):
            if isinstance(value, bool):
                return
            if isinstance(value, (int,)) and value >= 0:
                tokens[target] = int(value)

        # direct tokens dict
        raw_tokens = data.get("tokens")
        if isinstance(raw_tokens, dict):
            assign_if_int("prompt", raw_tokens.get("prompt"))
            assign_if_int("prompt", raw_tokens.get("input"))
            assign_if_int("prompt", raw_tokens.get("prompt_tokens"))
            assign_if_int("completion", raw_tokens.get("completion"))
            assign_if_int("completion", raw_tokens.get("output"))
            assign_if_int("completion", raw_tokens.get("completion_tokens"))
            assign_if_int("total", raw_tokens.get("total"))
            assign_if_int("total", raw_tokens.get("total_tokens"))

        # usage block commonly used by APIs
        usage = data.get("usage")
        if isinstance(usage, dict):
            assign_if_int("prompt", usage.get("prompt_tokens"))
            assign_if_int("completion", usage.get("completion_tokens"))
            assign_if_int("total", usage.get("total_tokens"))

        # flat fields
        assign_if_int("prompt", data.get("prompt_tokens"))
        assign_if_int("completion", data.get("completion_tokens"))
        assign_if_int("total", data.get("total_tokens"))

        # compute totals if missing or inconsistent
        if tokens["total"] <= 0:
            total = 0
            if tokens["prompt"] > 0:
                total += tokens["prompt"]
            if tokens["completion"] > 0:
                total += tokens["completion"]
            tokens["total"] = total

        # If we only have total, keep prompt/completion as 0
        return tokens

    def _calculate_cost_safe(self, model: str, tokens: Dict[str, int], mode: "CostMode") -> Optional[float]:
        calc = self._pricing_calculator
        prompt = tokens.get("prompt", 0)
        completion = tokens.get("completion", 0)
        total = tokens.get("total", 0)

        # Try common method signatures
        try:
            if hasattr(calc, "calculate"):
                try:
                    # type: ignore[attr-defined]
                    return float(calc.calculate(model=model, prompt_tokens=prompt, completion_tokens=completion, mode=mode))
                except TypeError:
                    pass
                try:
                    # type: ignore[misc]
                    return float(calc.calculate(model, prompt, completion, mode))
                except TypeError:
                    pass
                try:
                    # type: ignore[attr-defined]
                    return float(calc.calculate(model=model, total_tokens=total, mode=mode))
                except TypeError:
                    pass
        except Exception:
            pass

        try:
            if hasattr(calc, "calculate_cost"):
                try:
                    # type: ignore[attr-defined]
                    return float(calc.calculate_cost(model=model, prompt_tokens=prompt, completion_tokens=completion, mode=mode))
                except TypeError:
                    pass
                try:
                    # type: ignore[misc]
                    return float(calc.calculate_cost(model, total, mode))
                except TypeError:
                    pass
        except Exception:
            pass

        return None

    def _build_usage_entry_safe(
        self,
        timestamp: datetime,
        model: str,
        tokens: Dict[str, int],
        cost: Optional[float],
        mode: "CostMode",
        metadata: Dict[str, str],
    ) -> Optional["UsageEntry"]:
        prompt = tokens.get("prompt", 0)
        completion = tokens.get("completion", 0)
        total = tokens.get("total", 0)

        # Try multiple constructors to maximize compatibility
        ctor_attempts = [
            # Most descriptive kwargs
            dict(
                timestamp=timestamp,
                model=model,
                input_tokens=prompt,
                output_tokens=completion,
                total_tokens=total,
                cost=cost,
                mode=mode,
                metadata=metadata,
            ),
            # tokens dict variant
            dict(
                timestamp=timestamp,
                model=model,
                tokens=tokens,
                cost=cost,
                mode=mode,
                metadata=metadata,
            ),
            # Without mode
            dict(
                timestamp=timestamp,
                model=model,
                tokens=tokens,
                cost=cost,
                metadata=metadata,
            ),
            # Positional: timestamp, model, tokens, cost, mode, metadata
            ("positional", (timestamp, model, tokens, cost, mode, metadata)),
            # Positional reduced
            ("positional", (timestamp, model, tokens, cost)),
        ]

        UsageEntry = self._get_usage_entry_type()
        if UsageEntry is None:
            return None

        for attempt in ctor_attempts:
            try:
                if isinstance(attempt, dict):
                    return UsageEntry(**attempt)  # type: ignore[call-arg]
                else:
                    _, args = attempt
                    return UsageEntry(*args)  # type: ignore[misc]
            except Exception:
                continue
        return None

    def _get_usage_entry_type(self):
        try:
            from typing import TYPE_CHECKING  # noqa: F401
        except Exception:
            pass
        try:
            # If UsageEntry is available in globals (type hints), resolve it
            return globals().get("UsageEntry") or locals().get("UsageEntry")
        except Exception:
            return None

    def _ensure_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            # Delegate to handler if it can attach timezone
            try:
                if hasattr(self._timezone_handler, "ensure_timezone"):
                    dt2 = self._timezone_handler.ensure_timezone(
                        dt)  # type: ignore[attr-defined]
                    if isinstance(dt2, datetime):
                        dt = dt2
            except Exception:
                pass
            return dt.replace(tzinfo=timezone.utc)
        try:
            # Convert to UTC via handler if available
            if hasattr(self._timezone_handler, "to_utc"):
                dt2 = self._timezone_handler.to_utc(
                    dt)  # type: ignore[attr-defined]
                if isinstance(dt2, datetime):
                    return dt2
        except Exception:
            pass
        return dt.astimezone(timezone.utc)

    def _to_str(self, v: Any) -> str:
        if isinstance(v, str):
            return v
        if isinstance(v, (int, float, bool)):
            return str(v)
        if isinstance(v, datetime):
            return v.isoformat()
        # Avoid large dumps
        try:
            return str(v)
        except Exception:
            return ""
