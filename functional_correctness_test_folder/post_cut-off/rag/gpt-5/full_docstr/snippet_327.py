from __future__ import annotations

from typing import Any, Optional, Dict
import json

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.json import JSON
    from rich.text import Text
except Exception:  # pragma: no cover
    # Fallback stubs if rich is not available during static analysis
    Console = Any  # type: ignore
    Panel = Any  # type: ignore
    Columns = Any  # type: ignore
    JSON = Any  # type: ignore
    Text = Any  # type: ignore


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: "Event", console: "Console") -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # Attempt to interpret event as a function call
        function_call = self._extract_function_call(obj)
        if function_call is not None:
            self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        # Attempt to interpret event as a function response
        response = self._extract_function_response(obj)
        if response is not None:
            # Group with pending call if available
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                # Render response standalone
                console.print(self._make_response_panel(response))
            return

        # Generic event: flush pending call and print event as-is
        self._flush_pending_function_call(console)
        console.print(obj)

    def _flush_pending_function_call(self, console: "Console") -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is None:
            return
        call = self._pending_function_call
        self._pending_function_call = None

        call_name = self._get_function_name(call)
        call_args = self._get_function_arguments(call)

        left = self._make_call_panel(call_name, call_args, pending=True)
        console.print(left)

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: Dict[str, Any], console: "Console"
    ) -> None:
        """Render function call and response together in a grouped panel."""
        call_name = self._get_function_name(function_call)
        call_args = self._get_function_arguments(function_call)

        left = self._make_call_panel(call_name, call_args, pending=False)
        right = self._make_response_panel(response, call_name=call_name)

        try:
            columns = Columns([left, right], equal=True, expand=True)
            console.print(columns)
        except Exception:
            # Fallback if Columns isn't available/compatible
            console.print(left)
            console.print(right)

    # Helpers

    def _extract_function_call(self, event: Any) -> Optional[Any]:
        # Common shapes:
        # - event.function_call: FunctionCall
        # - event.type in {"function_call", "tool_call"} and event carries name/arguments
        # - event is itself a FunctionCall-like object with name/arguments
        if hasattr(event, "function_call") and getattr(event, "function_call") is not None:
            return getattr(event, "function_call")

        etype = getattr(event, "type", None) or getattr(
            event, "event_type", None)
        if etype in {"function_call", "tool_call"}:
            return event

        # Heuristic: object with name and arguments likely is a call
        if hasattr(event, "name") and (hasattr(event, "arguments") or hasattr(event, "args")):
            return event

        return None

    def _extract_function_response(self, event: Any) -> Optional[Dict[str, Any]]:
        # Common shapes:
        # - event.function_response: dict-like or object
        # - event.response or event.output or event.result
        # - event.type in {"function_response", "tool_response", "tool_result"}
        if hasattr(event, "function_response"):
            return self._to_dict(getattr(event, "function_response"))

        etype = getattr(event, "type", None) or getattr(
            event, "event_type", None)
        if etype in {"function_response", "tool_response", "tool_result"}:
            # Try common payload attributes
            for attr in ("response", "output", "result", "data", "value"):
                if hasattr(event, attr):
                    return self._to_dict(getattr(event, attr))
            # Fallback to event itself
            return self._to_dict(event)

        for attr in ("response", "output", "result"):
            if hasattr(event, attr):
                return self._to_dict(getattr(event, attr))

        return None

    def _get_function_name(self, call: Any) -> str:
        for attr in ("name", "function_name", "tool_name", "function", "method"):
            if hasattr(call, attr):
                val = getattr(call, attr)
                if val is not None:
                    return str(val)
        # Try dict-like
        if isinstance(call, dict):
            for key in ("name", "function_name", "tool_name", "function", "method"):
                if key in call and call[key] is not None:
                    return str(call[key])
        return call.__class__.__name__

    def _get_function_arguments(self, call: Any) -> Any:
        # Prefer typed attributes
        for attr in ("arguments", "args", "parameters", "kwargs", "params"):
            if hasattr(call, attr):
                val = getattr(call, attr)
                return self._maybe_parse_json(val)

        # Dict-like access
        if isinstance(call, dict):
            for key in ("arguments", "args", "parameters", "kwargs", "params"):
                if key in call:
                    return self._maybe_parse_json(call[key])

        return {}

    def _maybe_parse_json(self, val: Any) -> Any:
        if isinstance(val, (bytes, bytearray)):
            try:
                return json.loads(val.decode("utf-8"))
            except Exception:
                return val.decode("utf-8", errors="replace")
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                return parsed
            except Exception:
                return val
        return val

    def _to_dict(self, value: Any) -> Dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if hasattr(value, "model_dump"):
            try:
                dumped = value.model_dump()  # pydantic v2
                if isinstance(dumped, dict):
                    return dumped
            except Exception:
                pass
        if hasattr(value, "dict"):
            try:
                dumped = value.dict()  # pydantic v1
                if isinstance(dumped, dict):
                    return dumped
            except Exception:
                pass
        if hasattr(value, "__dict__"):
            try:
                return dict(value.__dict__)  # type: ignore[arg-type]
            except Exception:
                pass
        if isinstance(value, (str, bytes, bytearray)):
            parsed = self._maybe_parse_json(value)
            if isinstance(parsed, dict):
                return parsed
            return {"result": parsed}
        try:
            json.dumps(value)
            return {"result": value}
        except Exception:
            return {"result": repr(value)}

    def _make_call_panel(self, call_name: str, call_args: Any, pending: bool) -> Any:
        title = f"Function Call: {call_name}"
        if pending:
            subtitle = "pending response"
        else:
            subtitle = None

        body_renderable = self._json_renderable(call_args)
        try:
            return Panel(body_renderable, title=title, subtitle=subtitle, border_style="cyan")
        except Exception:
            return Panel(str(call_args), title=title, subtitle=subtitle)

    def _make_response_panel(self, response: Dict[str, Any], call_name: Optional[str] = None) -> Any:
        title = "Function Response" if call_name is None else f"Response: {call_name}"
        body_renderable = self._json_renderable(response)
        try:
            return Panel(body_renderable, title=title, border_style="green")
        except Exception:
            return Panel(str(response), title=title)

    def _json_renderable(self, obj: Any) -> Any:
        try:
            return JSON.from_data(obj)
        except Exception:
            try:
                return JSON(json.dumps(obj, ensure_ascii=False, default=str))
            except Exception:
                return Text(str(obj))
