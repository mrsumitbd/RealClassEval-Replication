from datetime import datetime, timezone
from typing import Any, Dict, Optional


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator, timezone_handler):
        self._pricing_calculator = pricing_calculator
        self._timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode):
        mapper_func = globals().get("_map_to_usage_entry")
        if callable(mapper_func):
            return mapper_func(
                data=data,
                pricing_calculator=self._pricing_calculator,
                timezone_handler=self._timezone_handler,
                mode=mode,
            )
        return None

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        if not isinstance(tokens, dict):
            return False
        try:
            total = tokens.get("total")
            if isinstance(total, int) and total > 0:
                return True
            # Fallback: sum known parts
            parts = 0
            for key in ("prompt", "completion", "cached", "input", "output"):
                val = tokens.get(key)
                if isinstance(val, int) and val >= 0:
                    parts += val
            return parts > 0
        except Exception:
            return False

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        value = (
            data.get("timestamp")
            or data.get("time")
            or (data.get("metadata") or {}).get("timestamp")
        )

        dt: Optional[datetime] = None

        if value is None:
            return None

        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, (int, float)):
            try:
                dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
            except Exception:
                dt = None
        elif isinstance(value, str):
            # Try ISO 8601 parsing
            try:
                # Handle 'Z' suffix
                if value.endswith("Z"):
                    value = value[:-1] + "+00:00"
                dt = datetime.fromisoformat(value)  # type: ignore[arg-type]
            except Exception:
                dt = None

        if dt is None:
            return None

        # Normalize to UTC using timezone_handler if available
        th = self._timezone_handler
        try:
            if hasattr(th, "to_utc") and callable(getattr(th, "to_utc")):
                return th.to_utc(dt)
            if hasattr(th, "normalize") and callable(getattr(th, "normalize")):
                return th.normalize(dt)
            if hasattr(th, "as_utc") and callable(getattr(th, "as_utc")):
                return th.as_utc(dt)
        except Exception:
            pass

        # Fallback: ensure UTC tzinfo
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        try:
            return dt.astimezone(timezone.utc)
        except Exception:
            return dt

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        model = data.get("model")
        if isinstance(model, str) and model:
            return model

        # Common fallbacks
        request = data.get("request") or {}
        if isinstance(request, dict):
            m = request.get("model")
            if isinstance(m, str) and m:
                return m

        meta = data.get("metadata") or data.get("meta") or {}
        if isinstance(meta, dict):
            m = meta.get("model")
            if isinstance(m, str) and m:
                return m

        # Another common key pattern
        usage = data.get("usage") or {}
        if isinstance(usage, dict):
            m = usage.get("model")
            if isinstance(m, str) and m:
                return m

        return ""

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        result: Dict[str, str] = {}

        # Primary metadata containers
        for key in ("metadata", "meta"):
            md = data.get(key)
            if isinstance(md, dict):
                for k, v in md.items():
                    if isinstance(k, str):
                        result[k] = v if isinstance(v, str) else str(v)

        # Common top-level fields to surface as metadata if not already present
        for k in ("request_id", "response_id", "session_id", "user_id", "project_id"):
            if k in data and k not in result:
                v = data[k]
                result[k] = v if isinstance(v, str) else str(v)

        return result
