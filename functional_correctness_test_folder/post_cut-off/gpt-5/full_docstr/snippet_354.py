from __future__ import annotations

from typing import Any, Optional, Mapping
from dataclasses import asdict, is_dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.pretty import Pretty
    from rich.text import Text
    from rich.table import Table
except Exception:  # Fallback shims if rich is not available
    class Console:  # type: ignore
        def print(self, *args, **kwargs):
            print(*args)

    class Panel:  # type: ignore
        def __init__(self, renderable, title: Optional[str] = None, subtitle: Optional[str] = None):
            self.renderable = renderable
            self.title = title
            self.subtitle = subtitle

        def __str__(self):
            title = f"[{self.title}]\n" if self.title else ""
            return f"{title}{self.renderable}"

    class Pretty:  # type: ignore
        def __init__(self, obj):
            self.obj = obj

        def __str__(self):
            return repr(self.obj)

    class Text(str):  # type: ignore
        pass

    class Table:  # type: ignore
        def __init__(self, title: Optional[str] = None, show_header: bool = False, box: Any = None):
            self.title = title
            self.rows = []

        def add_column(self, *_, **__):
            pass

        def add_row(self, *cols):
            self.rows.append(cols)

        def __str__(self):
            lines = []
            if self.title:
                lines.append(self.title)
            for row in self.rows:
                lines.append(" | ".join(map(str, row)))
            return "\n".join(lines)


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # If it's a function call event: store it pending (flushing any older pending)
        if self._looks_like_function_call_event(obj):
            self._flush_pending_function_call(console)
            self._pending_function_call = self._extract_function_call(obj)
            return

        # If it's a function response event: render grouped with pending if any
        if self._looks_like_function_response_event(obj):
            response = self._extract_function_response(obj)
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                self._render_response_standalone(response, console)
            return

        # For all other events, flush any pending call then render the event as-is.
        self._flush_pending_function_call(console)
        self._render_generic(obj, console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            fc = self._pending_function_call
            self._pending_function_call = None
            panel = Panel(self._render_function_call_pretty(
                fc), title="Function call (no response yet)")
            console.print(panel)

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        table = Table(show_header=False)
        table.add_column("k", ratio=1)
        table.add_column("v", ratio=3)

        table.add_row(
            Text("Call:"), self._render_function_call_pretty(function_call))
        table.add_row(Text("Response:"), Pretty(response))

        console.print(
            Panel(table, title=self._function_call_title(function_call)))

    # Helpers

    def _render_generic(self, obj: Any, console: 'Console') -> None:
        console.print(Pretty(self._to_primitive(obj)))

    def _render_response_standalone(self, response: dict[str, Any], console: 'Console') -> None:
        console.print(Panel(Pretty(response), title="Function response"))

    def _function_call_title(self, function_call: Any) -> str:
        # Try to extract a human-friendly title from function call
        name = None
        if isinstance(function_call, Mapping):
            name = function_call.get("name") or function_call.get(
                "function") or function_call.get("tool_name")
        else:
            name = getattr(function_call, "name", None) or getattr(
                function_call, "function", None)
        return f"Function call: {name}" if name else "Function call"

    def _render_function_call_pretty(self, function_call: Any) -> Any:
        # Show name and arguments nicely if available
        if isinstance(function_call, Mapping):
            name = function_call.get("name") or function_call.get(
                "function") or "unknown"
            args = function_call.get("arguments") or function_call.get(
                "args") or function_call.get("parameters")
            payload = {"name": name, "arguments": args}
            return Pretty(payload)
        else:
            name = getattr(function_call, "name", None) or getattr(
                function_call, "function", None)
            args = getattr(function_call, "arguments", None) or getattr(
                function_call, "args", None) or getattr(function_call, "parameters", None)
            payload = {"name": name, "arguments": self._to_primitive(args)}
            return Pretty(payload)

    def _looks_like_function_call_event(self, obj: Any) -> bool:
        # Explicit type markers
        t = self._get_type_str(obj)
        if t in {"function_call", "tool_call", "call"}:
            return True

        # Container with function_call attribute/key
        if hasattr(obj, "function_call"):
            return True
        if isinstance(obj, Mapping) and "function_call" in obj:
            return True

        # Looks like a FunctionCall object itself
        call_candidate = obj if not isinstance(
            obj, Mapping) else obj.get("function_call") or obj
        if self._has_function_signature(call_candidate):
            return True

        return False

    def _looks_like_function_response_event(self, obj: Any) -> bool:
        # Explicit type markers
        t = self._get_type_str(obj)
        if t in {"function_call_output", "function_result", "tool_output", "tool_result", "function_response", "call_result", "response"}:
            return True

        # Presence of a response-like payload
        if self._find_first_key(obj, ["function_call_output", "function_result", "tool_output", "function_response", "output", "result", "response"]) is not None:
            return True

        # Sometimes the object itself is the response mapping with 'role' tool and 'content'
        if isinstance(obj, Mapping) and (obj.get("role") in {"tool", "function"} and "content" in obj):
            return True

        return False

    def _extract_function_call(self, obj: Any) -> Any:
        if hasattr(obj, "function_call"):
            return getattr(obj, "function_call")
        if isinstance(obj, Mapping) and "function_call" in obj:
            return obj["function_call"]

        # If object itself looks like a call
        if self._has_function_signature(obj):
            return obj

        # Try common containers
        key = self._find_first_key(obj, ["call", "tool_call"])
        if key is not None:
            container = self._get_item(obj, key)
            if container is not None:
                return container

        return obj

    def _extract_function_response(self, obj: Any) -> dict[str, Any]:
        # Try common keys
        key = self._find_first_key(obj, ["function_call_output", "function_result", "tool_output",
                                   "tool_result", "function_response", "output", "result", "response"])
        if key is not None:
            val = self._get_item(obj, key)
            return self._to_mapping(val)

        # Some events place response under delta/data/payload
        key = self._find_first_key(obj, ["data", "payload", "delta"])
        if key is not None:
            val = self._get_item(obj, key)
            return self._to_mapping(val)

        # If object itself is a mapping, use it as the response
        if isinstance(obj, Mapping):
            return dict(obj)

        # Fallback to object dict or dataclass
        return self._to_mapping(obj)

    def _has_function_signature(self, candidate: Any) -> bool:
        if candidate is None:
            return False
        if isinstance(candidate, Mapping):
            if ("name" in candidate and ("arguments" in candidate or "args" in candidate or "parameters" in candidate)):
                return True
            # OpenAI style: tool_call with function: {type: function, function: {name, arguments}}
            if "function" in candidate and isinstance(candidate.get("function"), Mapping) and "name" in candidate["function"]:
                return True
            return False
        if hasattr(candidate, "name") and (hasattr(candidate, "arguments") or hasattr(candidate, "args") or hasattr(candidate, "parameters")):
            return True
        return False

    def _get_type_str(self, obj: Any) -> Optional[str]:
        val = None
        if hasattr(obj, "type"):
            val = getattr(obj, "type")
        elif isinstance(obj, Mapping) and "type" in obj:
            val = obj.get("type")
        if isinstance(val, str):
            return val.lower()
        return None

    def _find_first_key(self, obj: Any, keys: list[str]) -> Optional[str]:
        if isinstance(obj, Mapping):
            for k in keys:
                if k in obj:
                    return k
        else:
            for k in keys:
                if hasattr(obj, k):
                    return k
        return None

    def _get_item(self, obj: Any, key: str) -> Any:
        if isinstance(obj, Mapping):
            return obj.get(key)
        return getattr(obj, key, None)

    def _to_mapping(self, obj: Any) -> dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, Mapping):
            return dict(obj)
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "__dict__"):
            try:
                return dict(obj.__dict__)
            except Exception:
                pass
        return {"value": self._to_primitive(obj)}

    def _to_primitive(self, obj: Any) -> Any:
        if obj is None:
            return None
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, (list, tuple, set)):
            return [self._to_primitive(x) for x in obj]
        if isinstance(obj, Mapping):
            return {str(k): self._to_primitive(v) for k, v in obj.items()}
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "__dict__"):
            try:
                return {k: self._to_primitive(v) for k, v in vars(obj).items()}
            except Exception:
                pass
        try:
            return str(obj)
        except Exception:
            return repr(obj)
