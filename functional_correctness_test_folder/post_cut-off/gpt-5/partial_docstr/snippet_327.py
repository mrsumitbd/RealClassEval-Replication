from __future__ import annotations

from typing import Any, Optional, Dict
import json

try:
    from rich.console import Console
except Exception:  # Fallback type for environments without rich
    class Console:  # type: ignore
        def print(self, *args: Any, **kwargs: Any) -> None:
            print(*args)


class EventRenderer:
    def __init__(self) -> None:
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # Try to detect a function call or a function response within the event
        function_call = self._extract_function_call(obj)
        response = self._extract_function_response(obj)

        # If we received both in one event, render as a group
        if function_call is not None and response is not None:
            # If there is a different pending call, flush it first
            if self._pending_function_call is not None and self._pending_function_call is not function_call:
                self._flush_pending_function_call(console)
            self._render_function_call_group(function_call, response, console)
            return

        # If only a function call arrived, store it as pending
        if function_call is not None:
            # Flush any previous pending call before storing a new one
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        # If only a response arrived, try to pair with any pending function call
        if response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                # No function call to pair with; render the response standalone
                console.print("Function response:")
                console.print(self._stringify_json_like(response))
            return

        # If event is neither function call nor response, flush any pending call and render the event generically
        if self._pending_function_call is not None:
            self._flush_pending_function_call(console)

        # Generic fallback rendering for unknown events
        console.print(self._stringify_event(obj))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is None:
            return
        fc = self._pending_function_call
        name = self._get_attr(fc, "name") or "<unknown>"
        args = self._get_attr(fc, "arguments")
        console.print(
            f"Function call (no response): {name}{self._format_args(args)}")
        self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any] | dict, console: 'Console') -> None:
        name = self._get_attr(function_call, "name") or "<unknown>"
        args = self._get_attr(function_call, "arguments")
        console.print(f"Function call: {name}{self._format_args(args)}")
        console.print("Response:")
        console.print(self._stringify_json_like(response))

    # Helpers

    def _extract_function_call(self, obj: Any) -> Optional[Any]:
        # Direct FunctionCall object
        if obj is None:
            return None
        cls_name = obj.__class__.__name__
        # Direct FunctionCall instance
        if cls_name == "FunctionCall":
            return obj
        # Event with a function_call attribute
        if hasattr(obj, "function_call"):
            fc = getattr(obj, "function_call")
            if fc is not None:
                return fc
        # Some events might wrap a call under "call" or "tool_call"
        for attr in ("call", "tool_call", "tool", "fn_call"):
            if hasattr(obj, attr):
                candidate = getattr(obj, attr)
                if candidate is not None and hasattr(candidate, "name") and hasattr(candidate, "arguments"):
                    return candidate
        # Heuristic: dict-like event
        if isinstance(obj, dict):
            if isinstance(obj.get("function_call"), dict):
                return obj["function_call"]
            # OpenAI-like tool call structure
            tool_calls = obj.get("tool_calls")
            if isinstance(tool_calls, list) and tool_calls:
                call = tool_calls[0]
                if isinstance(call, dict) and "function" in call:
                    fn = call["function"]
                    if isinstance(fn, dict) and "name" in fn and "arguments" in fn:
                        return fn
        return None

    def _extract_function_response(self, obj: Any) -> Optional[Dict[str, Any]]:
        if obj is None:
            return None
        # If event itself is a known FunctionResponse-like class
        cls_name = obj.__class__.__name__
        if cls_name in {"FunctionResponse", "ToolResponse"}:
            payload = self._get_attr(obj, "response") or self._get_attr(
                obj, "output") or self._get_attr(obj, "result") or self._get_attr(obj, "content")
            if payload is None:
                return {}
            return self._ensure_dict(payload)
        # Attributes possibly carrying response payload
        for attr in ("function_response", "response", "output", "result", "content"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if val is not None:
                    return self._ensure_dict(val)
        # Dict-like
        if isinstance(obj, dict):
            for key in ("function_response", "response", "output", "result", "content"):
                if key in obj and obj[key] is not None:
                    return self._ensure_dict(obj[key])
        return None

    def _get_attr(self, obj: Any, attr: str) -> Any:
        try:
            return getattr(obj, attr)
        except Exception:
            return None

    def _format_args(self, args: Any) -> str:
        if args is None:
            return "()"
        # If args already a mapping or JSON string, show nicely
        if isinstance(args, str):
            # Try to pretty print if it's JSON
            try:
                parsed = json.loads(args)
                return f"({self._compact_json(parsed)})"
            except Exception:
                return f"({args})"
        if isinstance(args, (dict, list)):
            return f"({self._compact_json(args)})"
        return f"({repr(args)})"

    def _stringify_json_like(self, data: Any) -> str:
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        except Exception:
            return repr(data)

    def _compact_json(self, data: Any) -> str:
        try:
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        except Exception:
            return repr(data)

    def _ensure_dict(self, val: Any) -> Dict[str, Any]:
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, dict):
                    return parsed
                return {"data": parsed}
            except Exception:
                return {"data": val}
        # For list or other types, wrap it
        if isinstance(val, list):
            return {"data": val}
        return {"data": val}

    def _stringify_event(self, obj: Any) -> str:
        # Attempt a readable fallback representation
        try:
            if isinstance(obj, dict):
                return self._stringify_json_like(obj)
            # If event has a type and text/content, surface that
            etype = self._get_attr(obj, "type")
            text = self._get_attr(obj, "text") or self._get_attr(
                obj, "content") or self._get_attr(obj, "message")
            if etype or text:
                parts = []
                if etype:
                    parts.append(f"type={etype}")
                if text:
                    parts.append(f"text={text!r}")
                return "Event(" + ", ".join(parts) + ")"
            return repr(obj)
        except Exception:
            return repr(obj)
