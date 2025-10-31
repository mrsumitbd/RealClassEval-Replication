from __future__ import annotations

import json
from typing import Any, Optional


class EventRenderer:
    def __init__(self) -> None:
        self._pending_function_call: Optional[Any] = None
        self._pending_response: Optional[dict[str, Any]] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        function_call = self._extract_function_call(obj)
        response = self._extract_response(obj)
        text = self._extract_text(obj)

        if function_call is not None:
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            # If the same object also includes response, render immediately
            if response is not None:
                self._pending_response = response
                self._flush_pending_function_call(console)
            return

        if response is not None:
            if self._pending_function_call is not None:
                self._pending_response = response
                self._flush_pending_function_call(console)
            else:
                self._render_or_print(console, "Response:", response)
            return

        if text is not None:
            # Flush any pending function call before printing unrelated text
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._console_print(console, str(text))
            return

        # Unknown event; flush if needed and print a generic representation
        if self._pending_function_call is not None:
            self._flush_pending_function_call(console)
        self._console_print(console, str(obj))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self._pending_function_call is None:
            return
        try:
            self._render_function_call_group(
                self._pending_function_call,
                self._pending_response if self._pending_response is not None else {
                    "status": "no response"},
                console,
            )
        finally:
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        name = getattr(function_call, "name", None) or getattr(
            function_call, "tool_name", None) or "unknown"
        args = getattr(function_call, "arguments", None)
        if args is None and hasattr(function_call, "args"):
            args = getattr(function_call, "args")
        # Make args JSON-safe
        try:
            args_text = json.dumps(args, ensure_ascii=False, indent=2)
        except Exception:
            args_text = str(args)

        try:
            response_text = json.dumps(response, ensure_ascii=False, indent=2)
        except Exception:
            response_text = str(response)

        self._console_print(console, f"Function call: {name}")
        self._console_print(console, f"Arguments: {args_text}")
        self._console_print(console, f"Response: {response_text}")

    # Helpers

    def _render_or_print(self, console: 'Console', prefix: str, payload: Any) -> None:
        try:
            text = json.dumps(payload, ensure_ascii=False, indent=2)
        except Exception:
            text = str(payload)
        self._console_print(console, f"{prefix} {text}")

    def _console_print(self, console: 'Console', text: str) -> None:
        if hasattr(console, "print") and callable(getattr(console, "print")):
            console.print(text)
        elif hasattr(console, "write") and callable(getattr(console, "write")):
            console.write(text + "\n")
        elif hasattr(console, "log") and callable(getattr(console, "log")):
            console.log(text)
        else:
            # Last resort: try stdout-like interface
            try:
                console.write(text + "\n")  # type: ignore[attr-defined]
            except Exception:
                pass

    def _extract_function_call(self, obj: Any) -> Optional[Any]:
        if hasattr(obj, "function_call"):
            return getattr(obj, "function_call")
        # If the object itself looks like a function call
        if hasattr(obj, "name") and (hasattr(obj, "arguments") or hasattr(obj, "args")):
            return obj
        if hasattr(obj, "type") and getattr(obj, "type") == "function_call":
            data = getattr(obj, "data", None)
            if data is not None:
                return data
        return None

    def _extract_response(self, obj: Any) -> Optional[dict[str, Any]]:
        # Direct dict considered a response
        if isinstance(obj, dict):
            return obj
        for attr in ("response", "tool_response", "function_response", "result", "output"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, dict):
                    return val
        return None

    def _extract_text(self, obj: Any) -> Optional[str]:
        if isinstance(obj, str):
            return obj
        for attr in ("message", "text", "content"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, str):
                    return val
        return None
