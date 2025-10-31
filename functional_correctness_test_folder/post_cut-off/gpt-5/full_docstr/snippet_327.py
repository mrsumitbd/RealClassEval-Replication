from __future__ import annotations

from typing import Any, Optional
import json

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.columns import Columns
    from rich.rule import Rule
except Exception:  # Fallback stubs if rich isn't available at import time
    Console = Any
    Panel = Any
    Syntax = Any
    Text = Any
    Columns = Any
    Rule = Any


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # Identify if obj carries a function call or function response
        function_call = self._extract_function_call(obj)
        function_response = self._extract_function_response(obj)

        if function_call is not None:
            # If there is an unpaired pending call, flush it first
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        if function_response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, function_response, console)
                self._pending_function_call = None
            else:
                # No pending call; render response standalone
                self._render_function_call_group(
                    None, function_response, console)
            return

        # For other event types, flush any pending call and render the event plainly
        if self._pending_function_call is not None:
            self._flush_pending_function_call(console)

        self._render_generic_event(obj, console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is None:
            return
        call_text = self._format_function_call(self._pending_function_call)
        panel_title = "Function Call (pending response)"
        console.print(Panel(call_text, title=panel_title))
        self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall | None', response: dict[str, Any] | Any, console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        call_renderable = self._format_function_call(
            function_call) if function_call is not None else Text("No associated call", style="italic")
        resp_renderable = self._format_response(response)

        # Display side-by-side if console is wide enough; otherwise stacked
        try:
            columns = Columns([Panel(call_renderable, title="Function Call"), Panel(
                resp_renderable, title="Function Response")], expand=True, equal=True)
            console.print(columns)
        except Exception:
            console.print(Panel(call_renderable, title="Function Call"))
            console.print(Panel(resp_renderable, title="Function Response"))
        try:
            console.print(Rule())
        except Exception:
            pass

    # ---- Helpers ----

    def _render_generic_event(self, obj: Any, console: 'Console') -> None:
        title = self._infer_event_title(obj)
        body = self._infer_event_body(obj)
        console.print(Panel(body, title=title))

    def _infer_event_title(self, obj: Any) -> str:
        for attr in ("type", "event_type", "name", "role", "kind"):
            if hasattr(obj, attr):
                try:
                    val = getattr(obj, attr)
                    if val:
                        return str(val)
                except Exception:
                    continue
        return "Event"

    def _infer_event_body(self, obj: Any) -> Any:
        for attr in ("content", "message", "text", "data"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, (dict, list)):
                    return self._json_syntax(val)
                if val is not None:
                    return Text(str(val))
        # Fallback to string representation
        try:
            return Text(str(obj))
        except Exception:
            return Text(repr(obj))

    def _extract_function_call(self, obj: Any) -> Optional[Any]:
        # Common attribute patterns
        for attr in ("function_call", "tool_call", "call", "fn_call"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if val is not None:
                    return val
        # Sometimes events use a type discriminator
        if hasattr(obj, "type") and getattr(obj, "type") in ("function_call", "tool_call"):
            return getattr(obj, "payload", None) or getattr(obj, "data", None)
        return None

    def _extract_function_response(self, obj: Any) -> Optional[Any]:
        for attr in ("function_response", "tool_response", "response", "result", "output"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if val is not None:
                    return val
        if hasattr(obj, "type") and getattr(obj, "type") in ("function_response", "tool_response"):
            return getattr(obj, "payload", None) or getattr(obj, "data", None)
        return None

    def _format_function_call(self, function_call: Any) -> Any:
        if function_call is None:
            return Text("None")
        # Try common fields: name and arguments
        name = None
        args = None
        for n_attr in ("name", "function", "tool", "fn"):
            if hasattr(function_call, n_attr):
                try:
                    name = getattr(function_call, n_attr)
                    if isinstance(name, dict) and "name" in name:
                        name = name["name"]
                except Exception:
                    pass
                if name:
                    break
        for a_attr in ("arguments", "args", "parameters", "params"):
            if hasattr(function_call, a_attr):
                try:
                    args = getattr(function_call, a_attr)
                except Exception:
                    pass
                if args is not None:
                    break

        if name is None and isinstance(function_call, dict):
            name = function_call.get("name") or function_call.get(
                "function") or function_call.get("tool")
            args = function_call.get("arguments") or function_call.get(
                "args") or function_call.get("parameters") or function_call.get("params")

        if args is None and hasattr(function_call, "__dict__"):
            try:
                args = {k: v for k, v in vars(function_call).items(
                ) if k not in ("name", "function", "tool", "fn")}
            except Exception:
                args = None

        parts = []
        if name:
            parts.append(Text(str(name), style="bold"))
        if args is not None:
            try:
                parts.append(self._json_syntax(args))
            except Exception:
                parts.append(Text(str(args)))
        if not parts:
            return Text(str(function_call))
        try:
            from rich.console import Group
            return Group(*parts)
        except Exception:
            return Text(" ".join(str(p) for p in parts))

    def _format_response(self, response: Any) -> Any:
        if isinstance(response, (dict, list)):
            return self._json_syntax(response)
        # Some tool responses might carry a .content or .data
        for attr in ("content", "data", "text", "message"):
            if hasattr(response, attr):
                val = getattr(response, attr)
                if isinstance(val, (dict, list)):
                    return self._json_syntax(val)
                if val is not None:
                    return Text(str(val))
        return Text(str(response))

    def _json_syntax(self, data: Any) -> Any:
        try:
            dumped = json.dumps(
                data, indent=2, ensure_ascii=False, sort_keys=True)
            return Syntax(dumped, "json", theme="monokai", word_wrap=True)
        except Exception:
            return Text(str(data))
