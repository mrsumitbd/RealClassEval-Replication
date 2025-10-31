from typing import Optional, Dict, Any
from datetime import datetime, timezone


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: "PricingCalculator", timezone_handler: "TimezoneHandler"):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: "CostMode") -> Optional["UsageEntry"]:
        '''Map raw data to UsageEntry - compatibility interface.'''
        if not isinstance(data, dict):
            return None

        tokens = data.get("tokens") or {}
        if not isinstance(tokens, dict):
            tokens = {}

        if not self._has_valid_tokens(tokens):
            return None

        mapper = getattr(self, "_map_to_usage_entry", None)
        if not callable(mapper):
            # Try resolve from module/global scope if provided elsewhere
            mapper = globals().get("_map_to_usage_entry")
        if callable(mapper):
            try:
                return mapper(data, mode, self.pricing_calculator, self.timezone_handler)
            except Exception:
                pass

        # Fallback minimal construction if the functional mapper is not available
        try:
            ts = self._extract_timestamp(data)
            model = self._extract_model(data)
            metadata = self._extract_metadata(data)

            # Optional cost computation if supported by the calculator
            cost = None
            calc = getattr(self.pricing_calculator, "calculate_cost", None)
            if callable(calc):
                try:
                    cost = calc(model=model, tokens=tokens,
                                mode=mode, metadata=metadata)
                except Exception:
                    cost = None

            # Try to instantiate UsageEntry in a flexible manner
            UsageEntryCls = globals().get("UsageEntry")
            if UsageEntryCls is None:
                return None

            try:
                return UsageEntryCls(
                    timestamp=ts,
                    model=model,
                    tokens=tokens,
                    cost=cost,
                    mode=mode,
                    metadata=metadata,
                )
            except TypeError:
                try:
                    return UsageEntryCls(ts, model, tokens, cost, mode, metadata)
                except Exception:
                    return None
        except Exception:
            return None

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict):
            return False

        def _is_pos_int(x: Any) -> bool:
            return isinstance(x, int) and x >= 0

        # Accept either explicit total or sum of prompt/completion
        total = tokens.get("total")
        prompt = tokens.get("prompt")
        completion = tokens.get("completion")

        if _is_pos_int(total):
            return True

        # If either prompt or completion exists, ensure both (if present) are valid
        any_present = ("prompt" in tokens) or ("completion" in tokens)
        if any_present:
            if (prompt is None or _is_pos_int(prompt)) and (completion is None or _is_pos_int(completion)):
                # Consider zero acceptable
                return True

        # Some systems use 'input'/'output'
        input_t = tokens.get("input")
        output_t = tokens.get("output")
        any_io_present = ("input" in tokens) or ("output" in tokens)
        if any_io_present:
            if (input_t is None or _is_pos_int(input_t)) and (output_t is None or _is_pos_int(output_t)):
                return True

        return False

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        ts = (
            data.get("timestamp")
            or data.get("created")
            or data.get("time")
            or (data.get("usage") or {}).get("timestamp")
        )

        dt: Optional[datetime] = None

        if isinstance(ts, datetime):
            dt = ts
        elif isinstance(ts, (int, float)):
            try:
                dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
            except Exception:
                dt = None
        elif isinstance(ts, str):
            s = ts.strip()
            try:
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                dt = None

        # Attempt to use timezone handler if available to normalize
        try:
            if dt is not None and self.timezone_handler is not None:
                # Prefer method named normalize or to_utc if present
                if hasattr(self.timezone_handler, "normalize") and callable(self.timezone_handler.normalize):
                    dt = self.timezone_handler.normalize(dt)
                elif hasattr(self.timezone_handler, "to_utc") and callable(self.timezone_handler.to_utc):
                    dt = self.timezone_handler.to_utc(dt)
        except Exception:
            pass

        return dt

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        model = (
            data.get("model")
            or (data.get("request") or {}).get("model")
            or (data.get("metadata") or {}).get("model")
            or (data.get("usage") or {}).get("model")
        )
        if isinstance(model, str) and model.strip():
            return model.strip()
        return "unknown"

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        md_raw = data.get("metadata") or {}
        if not isinstance(md_raw, dict):
            md_raw = {}

        metadata: Dict[str, str] = {}

        # Copy string-able key/values from provided metadata
        for k, v in md_raw.items():
            try:
                ks = str(k)
                vs = "" if v is None else str(v)
                metadata[ks] = vs
            except Exception:
                continue

        # Common top-level identifiers promoted to metadata for compatibility
        for k in ("user_id", "user", "request_id", "trace_id", "organization", "org", "project"):
            if k in data and k not in metadata:
                try:
                    metadata[k] = "" if data[k] is None else str(data[k])
                except Exception:
                    pass

        # Include model if not already present
        if "model" not in metadata and "model" in data:
            try:
                metadata["model"] = str(data["model"])
            except Exception:
                pass

        return metadata
