from __future__ import annotations

from typing import Any, Optional, Mapping

import json

try:
    from rich.panel import Panel
    from rich.pretty import Pretty
    from rich.console import Group
except Exception:  # pragma: no cover - fallback if rich components unavailable
    Panel = None  # type: ignore
    Pretty = None  # type: ignore
    Group = None  # type: ignore


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call: Optional["FunctionCall"] = None

    def render_event(self, obj: "Event", console: "Console") -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # Try to extract function call and function response from the event
        function_call = self._extract_function_call(obj)
        function_response = self._extract_function_response(obj)

        if function_call is not None:
            # If we already have a pending call, flush it before queuing a new one
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        if function_response is not None:
            # If this is a response and we have a pending call, render them together
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, function_response, console)
                self._pending_function_call = None
                return
            # No pending call; render response standalone
            self._render_standalone_response(function_response, console)
            return

        # Any other event: flush pending function call first, then render the event generically
        self._flush_pending_function_call(console)
        self._render_generic_event(obj, console)

    def _flush_pending_function_call(self, console: "Console") -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is None:
            return

        fc = self._pending_function_call
        name = self._get_function_call_name(fc)
        args = self._get_function_call_args(fc)

        if Panel and Pretty:
            content = Pretty({"name": name, "args": args}, expand_all=True)
            console.print(
                Panel(content, title="Function Call (no response yet)", border_style="yellow"))
        else:  # Fallback if rich components failed to import
            console.print(
                f"Function Call (no response yet): name={name}, args={args}")

        self._pending_function_call = None

    def _render_function_call_group(self, function_call: "FunctionCall", response: dict[str, Any], console: "Console") -> None:
        """Render function call and response together in a grouped panel."""
        name = self._get_function_call_name(function_call)
        args = self._get_function_call_args(function_call)

        if Panel and Pretty and Group:
            call_panel = Panel(Pretty(
                {"name": name, "args": args}, expand_all=True), title="Function Call", border_style="cyan")
            resp_panel = Panel(Pretty(response, expand_all=True),
                               title="Function Response", border_style="green")
            console.print(Panel(Group(call_panel, resp_panel),
                          title=f"Function: {name}", border_style="magenta"))
        else:  # Fallback
            console.print(f"Function: {name}")
            console.print(f"  Call args: {args}")
            console.print(f"  Response: {response}")

    # Helpers

    def _extract_function_call(self, event: Any) -> Optional["FunctionCall"]:
        # Common attributes
        if hasattr(event, "function_call"):
            return getattr(event, "function_call")
        if hasattr(event, "call"):
            return getattr(event, "call")
        # Dictionary-like
        if isinstance(event, Mapping):
            if "function_call" in event:
                return event["function_call"]  # type: ignore[return-value]
            if "call" in event:
                return event["call"]  # type: ignore[return-value]
            # Sometimes events might be tagged with types
            etype = event.get("type") or event.get("event")
            if (etype or "").lower() in ("function_call", "functioncall", "call"):
                # type: ignore[return-value]
                return event.get("data") or event.get("payload") or event.get("function")
        return None

    def _extract_function_response(self, event: Any) -> Optional[dict[str, Any]]:
        # Common attributes
        if hasattr(event, "function_response"):
            return self._to_dict(getattr(event, "function_response"))
        if hasattr(event, "response"):
            return self._to_dict(getattr(event, "response"))
        # Dictionary-like
        if isinstance(event, Mapping):
            if "function_response" in event:
                return self._to_dict(event["function_response"])
            if "response" in event and isinstance(event["response"], (dict, object)):
                return self._to_dict(event["response"])
            etype = event.get("type") or event.get("event")
            if (etype or "").lower() in ("function_response", "functionresponse", "response"):
                payload = event.get("data") or event.get(
                    "payload") or event.get("result")
                return self._to_dict(payload)
        return None

    def _get_function_call_name(self, function_call: Any) -> str:
        # Try common name attributes
        for attr in ("name", "function_name", "fn_name", "id"):
            if hasattr(function_call, attr):
                val = getattr(function_call, attr)
                if isinstance(val, str):
                    return val
        # Mapping
        if isinstance(function_call, Mapping):
            for key in ("name", "function_name", "fn_name", "id"):
                val = function_call.get(key)
                if isinstance(val, str):
                    return val
        # Fallback
        return type(function_call).__name__

    def _get_function_call_args(self, function_call: Any) -> Any:
        # Try typical attributes
        for attr in ("args", "arguments", "parameters", "params"):
            if hasattr(function_call, attr):
                val = getattr(function_call, attr)
                return self._parse_args(val)
        # Mapping
        if isinstance(function_call, Mapping):
            for key in ("args", "arguments", "parameters", "params"):
                if key in function_call:
                    return self._parse_args(function_call[key])
        # Fallback
        return {}

    def _parse_args(self, args: Any) -> Any:
        # If it's a JSON string, try to decode
        if isinstance(args, str):
            try:
                return json.loads(args)
            except Exception:
                return args
        return args

    def _to_dict(self, obj: Any) -> Optional[dict[str, Any]]:
        if obj is None:
            return None
        if isinstance(obj, Mapping):
            return dict(obj)
        # Try common conversion methods
        for method in ("to_dict", "model_dump", "dict"):
            fn = getattr(obj, method, None)
            if callable(fn):
                try:
                    res = fn()
                    if isinstance(res, Mapping):
                        return dict(res)
                except Exception:
                    pass
        # As a last resort, use __dict__ if it looks meaningful
        d = getattr(obj, "__dict__", None)
        if isinstance(d, dict) and d:
            return dict(d)
        # Wrap unknown payload
        return {"value": obj}

    def _render_standalone_response(self, response: dict[str, Any], console: "Console") -> None:
        if Panel and Pretty:
            console.print(Panel(Pretty(response, expand_all=True),
                          title="Function Response", border_style="green"))
        else:
            console.print(f"Function Response: {response}")

    def _render_generic_event(self, event: Any, console: "Console") -> None:
        # Try to pretty print mapping-like events; otherwise print raw
        if isinstance(event, Mapping) and Panel and Pretty:
            console.print(Panel(Pretty(dict(event), expand_all=True),
                          title="Event", border_style="blue"))
        else:
            console.print(event)
