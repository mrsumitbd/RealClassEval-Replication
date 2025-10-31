from typing import Any, Optional, Mapping


class EventRenderer:
    def __init__(self) -> None:
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        evt_type = self._extract_type(obj)

        if evt_type in ("function_call", "tool_call", "call"):
            # Flush any previous dangling call
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = self._extract_function_call(obj)
            if self._pending_function_call is None:
                # If we can't extract it, just print the event
                self._safe_print(console, self._format_generic(obj))
        elif evt_type in ("function_result", "function_response", "tool_result", "response"):
            response = self._extract_response(obj)
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                # No pending call, render standalone
                self._safe_print(
                    console, f"Function response: {self._format_response(response)}")
        else:
            # For any other event, flush pending and print generic
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._safe_print(console, self._format_generic(obj))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self._pending_function_call is not None:
            fc = self._pending_function_call
            self._safe_print(
                console, f"Function call: {self._format_function_call(fc)}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        self._safe_print(
            console, f"Function call: {self._format_function_call(function_call)}")
        self._safe_print(
            console, f"Function response: {self._format_response(response)}")

    def _safe_print(self, console: Any, message: str) -> None:
        try:
            if console is not None and hasattr(console, "print"):
                console.print(message)
            else:
                print(message)
        except Exception:
            print(message)

    def _extract_type(self, obj: Any) -> Optional[str]:
        if obj is None:
            return None
        if isinstance(obj, Mapping):
            return obj.get("type") or obj.get("event") or obj.get("kind")
        return getattr(obj, "type", None) or getattr(obj, "event", None) or getattr(obj, "kind", None)

    def _extract_function_call(self, obj: Any) -> Any:
        if obj is None:
            return None
        if isinstance(obj, Mapping):
            if "function_call" in obj:
                return obj.get("function_call")
            if "data" in obj and isinstance(obj["data"], Mapping) and "function_call" in obj["data"]:
                return obj["data"]["function_call"]
            if "call" in obj:
                return obj.get("call")
            if "tool_call" in obj:
                return obj.get("tool_call")
        # Attribute-based extraction
        for attr in ("function_call", "call", "tool_call"):
            if hasattr(obj, attr):
                return getattr(obj, attr)
        data = getattr(obj, "data", None)
        if isinstance(data, Mapping) and "function_call" in data:
            return data["function_call"]
        return None

    def _extract_response(self, obj: Any) -> dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, Mapping):
            if "response" in obj and isinstance(obj["response"], Mapping):
                return obj["response"]  # type: ignore[return-value]
            if "data" in obj and isinstance(obj["data"], Mapping):
                resp = obj["data"].get("response")
                if isinstance(resp, Mapping):
                    return resp  # type: ignore[return-value]
                # Sometimes the data itself is the response
                return obj["data"]  # type: ignore[return-value]
            # Fallback: treat entire mapping as response
            return obj  # type: ignore[return-value]
        # Attribute-based
        resp = getattr(obj, "response", None)
        if isinstance(resp, Mapping):
            return resp  # type: ignore[return-value]
        data = getattr(obj, "data", None)
        if isinstance(data, Mapping):
            inner = data.get("response")
            if isinstance(inner, Mapping):
                return inner  # type: ignore[return-value]
            return data  # type: ignore[return-value]
        return {}

    def _format_function_call(self, function_call: Any) -> str:
        if function_call is None:
            return "<unknown>"
        # If mapping-like
        if isinstance(function_call, Mapping):
            name = function_call.get("name") or function_call.get(
                "tool_name") or function_call.get("fn") or "unknown"
            args = function_call.get("arguments") or function_call.get(
                "args") or function_call.get("input") or {}
        else:
            name = getattr(function_call, "name", None) or getattr(
                function_call, "tool_name", None) or getattr(function_call, "fn", None) or "unknown"
            args = getattr(function_call, "arguments", None) or getattr(
                function_call, "args", None) or getattr(function_call, "input", None) or {}
        try:
            import json
            args_str = json.dumps(args, ensure_ascii=False)
        except Exception:
            args_str = str(args)
        return f"{name}({args_str})"

    def _format_response(self, response: Any) -> str:
        try:
            import json
            return json.dumps(response, ensure_ascii=False)
        except Exception:
            return str(response)

    def _format_generic(self, obj: Any) -> str:
        evt_type = self._extract_type(obj) or "event"
        if isinstance(obj, Mapping):
            payload = {k: v for k, v in obj.items(
            ) if k not in ("type", "event", "kind")}
        else:
            payload = getattr(obj, "__dict__", {}) or obj
        try:
            import json
            payload_str = json.dumps(payload, ensure_ascii=False, default=str)
        except Exception:
            payload_str = str(payload)
        return f"{evt_type}: {payload_str}"
