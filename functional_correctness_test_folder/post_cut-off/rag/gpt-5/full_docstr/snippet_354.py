from typing import Any, Optional, Dict
import json
from dataclasses import asdict, is_dataclass


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # Detect a function call event.
        function_call = self._extract_function_call(obj)
        if function_call is not None:
            # If a previous call is pending, flush it before taking a new one.
            self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        # Detect a function call response event.
        response = self._extract_function_response(obj)
        if response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                # No pending call; render the response alone.
                self._render_standalone_response(response, console)
            return

        # For any other event types, flush pending and render generic content.
        self._flush_pending_function_call(console)
        self._render_generic_event(obj, console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is None:
            return
        call = self._pending_function_call
        name = self._safe_get(
            call, ['name', 'function', 'tool_name'], default='unknown')
        args = self._safe_get(
            call, ['args', 'arguments', 'parameters'], default={})
        formatted_args = self._format_json(args)
        try:
            from rich.panel import Panel
            from rich.syntax import Syntax
            from rich.text import Text
            call_header = Text(
                "Function Call (no response yet)", style="bold yellow")
            call_body = Text.assemble(
                ("name: ", "bold"),
                (str(name),),
                ("\nargs:\n", "bold"),
            )
            call_args = Syntax(formatted_args, "json",
                               theme="ansi_dark", word_wrap=True)
            console.print(Panel.fit(Group(call_header, call_body,
                          call_args), border_style="yellow"))
        except Exception:
            console.print("=== Function Call (no response yet) ===")
            console.print(f"name: {name}")
            console.print("args:")
            console.print(formatted_args)
            console.print("=======================================")
        finally:
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        """Render function call and response together in a grouped panel."""
        name = self._safe_get(
            function_call, ['name', 'function', 'tool_name'], default='unknown')
        args = self._safe_get(
            function_call, ['args', 'arguments', 'parameters'], default={})
        call_id = self._safe_get(
            function_call, ['id', 'call_id'], default=None)

        formatted_args = self._format_json(args)
        formatted_response = self._format_json(response)

        try:
            from rich.panel import Panel
            from rich.columns import Columns
            from rich.syntax import Syntax
            from rich.text import Text
            from rich.align import Align
            from rich.console import Group

            title_suffix = f" [{call_id}]" if call_id is not None else ""
            call_title = f"Function Call: {name}{title_suffix}"
            resp_title = "Function Response"

            call_renderable = Group(
                Text(f"name: {name}", style="bold"),
                Text(f"id: {call_id}") if call_id is not None else Text(""),
                Text("args:", style="bold"),
                Syntax(formatted_args, "json",
                       theme="ansi_dark", word_wrap=True),
            )
            resp_renderable = Group(
                Text("response:", style="bold"),
                Syntax(formatted_response, "json",
                       theme="ansi_dark", word_wrap=True),
            )

            call_panel = Panel(
                call_renderable, title=call_title, border_style="cyan")
            resp_panel = Panel(
                resp_renderable, title=resp_title, border_style="green")

            console.print(
                Columns([call_panel, resp_panel], expand=True, equal=True))
        except Exception:
            # Fallback plain text rendering
            separator = "-" * 40
            console.print(
                f"{separator}\nFunction Call: {name} {f'(id: {call_id})' if call_id else ''}")
            console.print("args:")
            console.print(formatted_args)
            console.print("Function Response:")
            console.print(formatted_response)
            console.print(separator)

    def _render_standalone_response(self, response: Dict[str, Any], console: 'Console') -> None:
        formatted_response = self._format_json(response)
        try:
            from rich.panel import Panel
            from rich.syntax import Syntax
            from rich.text import Text
            from rich.console import Group
            header = Text("Function Response (unpaired)", style="bold green")
            body = Syntax(formatted_response, "json",
                          theme="ansi_dark", word_wrap=True)
            console.print(Panel.fit(Group(header, body), border_style="green"))
        except Exception:
            console.print("=== Function Response (unpaired) ===")
            console.print(formatted_response)
            console.print("====================================")

    def _render_generic_event(self, obj: Any, console: 'Console') -> None:
        # Try to display useful fields if present, else fallback to repr.
        text = None
        if hasattr(obj, "text"):
            text = getattr(obj, "text")
        elif hasattr(obj, "message"):
            text = getattr(obj, "message")
        elif hasattr(obj, "data") and isinstance(getattr(obj, "data"), str):
            text = getattr(obj, "data")

        try:
            from rich.panel import Panel
            from rich.text import Text as RichText
            if text is not None:
                console.print(
                    Panel.fit(RichText(str(text)), border_style="white"))
            else:
                console.print(
                    Panel.fit(RichText(repr(obj)), border_style="white"))
        except Exception:
            if text is not None:
                console.print(str(text))
            else:
                console.print(repr(obj))

    def _extract_function_call(self, obj: Any) -> Optional[Any]:
        # Common patterns: obj.function_call, obj.data (with name/args), obj.payload, etc.
        if hasattr(obj, "function_call"):
            return getattr(obj, "function_call")
        if hasattr(obj, "data"):
            data = getattr(obj, "data")
            if data is not None and self._looks_like_function_call(data):
                return data
        if hasattr(obj, "payload"):
            payload = getattr(obj, "payload")
            if payload is not None and self._looks_like_function_call(payload):
                return payload
        # Sometimes type attribute hints at function call
        if getattr(obj, "type", "").lower() in {"function_call", "tool_call"} and hasattr(obj, "data"):
            if self._looks_like_function_call(getattr(obj, "data")):
                return getattr(obj, "data")
        return None

    def _extract_function_response(self, obj: Any) -> Optional[Dict[str, Any]]:
        # Common patterns: obj.function_response, obj.response, obj.data: dict
        candidate = None
        if hasattr(obj, "function_response"):
            candidate = getattr(obj, "function_response")
        elif hasattr(obj, "response"):
            candidate = getattr(obj, "response")
        elif hasattr(obj, "data"):
            data = getattr(obj, "data")
            if isinstance(data, dict):
                candidate = data

        if candidate is None:
            return None

        if isinstance(candidate, dict):
            return candidate
        if is_dataclass(candidate):
            return asdict(candidate)
        if hasattr(candidate, "__dict__"):
            return dict(candidate.__dict__)

        # Fallback: best-effort serialization
        try:
            json.dumps(candidate, default=repr)
            return {"value": candidate}
        except Exception:
            return {"value": repr(candidate)}

    def _looks_like_function_call(self, obj: Any) -> bool:
        # Heuristic: has a name and some argument-like attribute.
        has_name = any(hasattr(obj, attr)
                       for attr in ("name", "function", "tool_name"))
        has_args = any(hasattr(obj, attr)
                       for attr in ("args", "arguments", "parameters"))
        return has_name and has_args

    def _safe_get(self, obj: Any, attrs: list[str], default: Any = None) -> Any:
        for attr in attrs:
            if hasattr(obj, attr):
                return getattr(obj, attr)
        return default

    def _format_json(self, value: Any) -> str:
        # Normalize value to something JSON serializable for display.
        if is_dataclass(value):
            value = asdict(value)
        elif hasattr(value, "__dict__") and not isinstance(value, dict):
            value = dict(value.__dict__)
        try:
            return json.dumps(value, indent=2, ensure_ascii=False, default=self._json_default)
        except Exception:
            # If it still fails, fall back to repr
            return repr(value)

    def _json_default(self, obj: Any) -> Any:
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return repr(obj)


# Helper for Group import inside methods where needed
try:
    from rich.console import Group  # type: ignore
except Exception:
    class Group:  # type: ignore
        def __init__(self, *args: Any) -> None:
            self._children = args
