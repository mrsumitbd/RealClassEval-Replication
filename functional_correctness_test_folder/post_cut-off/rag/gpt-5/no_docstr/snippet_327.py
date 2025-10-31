from typing import Any, Optional, Dict, Tuple

import json

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.syntax import Syntax
except Exception:  # pragma: no cover
    # Fallback stubs if rich is not available at runtime, to avoid import errors in non-rendering contexts.
    class Console:  # type: ignore
        def print(self, *args: Any, **kwargs: Any) -> None:
            pass

    class Group:  # type: ignore
        def __init__(self, *children: Any) -> None:
            self.children = children

    class Panel:  # type: ignore
        def __init__(self, renderable: Any, title: Optional[str] = None, border_style: Optional[str] = None, padding: Any = None) -> None:
            self.renderable = renderable
            self.title = title
            self.border_style = border_style
            self.padding = padding

    class Syntax:  # type: ignore
        def __init__(self, code: str, lexer: str, theme: Optional[str] = None, line_numbers: bool = False, word_wrap: bool = False) -> None:
            self.code = code
            self.lexer = lexer
            self.theme = theme
            self.line_numbers = line_numbers
            self.word_wrap = word_wrap


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # If a new function call arrives while one is pending, flush the previous unpaired call.
        if self._is_function_call_event(obj):
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = self._extract_function_call(obj)
            return

        # If a function response arrives, pair and render with pending call (if any).
        response = self._extract_function_response(obj)
        if response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                # No pending call: just render the response by itself.
                self._render_function_call_group(None, response, console)
            return

        # For all other events, flush any pending call and then print the event directly.
        self._flush_pending_function_call(console)
        try:
            console.print(obj)
        except Exception:
            # Fallback to a safe representation
            console.print(str(obj))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is None:
            return
        name, args = self._coerce_function_call(self._pending_function_call)
        call_payload = {"name": name, "arguments": args}
        call_json = self._to_pretty_json(call_payload)

        call_panel = Panel(
            Syntax(call_json, "json", theme="monokai",
                   line_numbers=False, word_wrap=True),
            title="Function Call (unpaired)",
            border_style="blue",
            padding=(1, 2),
        )
        main_panel = Panel(call_panel, title="Tool Invocation",
                           border_style="cyan", padding=1)
        console.print(main_panel)
        self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        # Render call section
        call_panel: Optional[Panel] = None
        if function_call is not None:
            name, args = self._coerce_function_call(function_call)
            call_payload = {"name": name, "arguments": args}
            call_json = self._to_pretty_json(call_payload)
            call_panel = Panel(
                Syntax(call_json, "json", theme="monokai",
                       line_numbers=False, word_wrap=True),
                title="Function Call",
                border_style="blue",
                padding=(1, 2),
            )

        # Render response section
        response_json = self._to_pretty_json(self._coerce_to_dict(response))
        response_panel = Panel(
            Syntax(response_json, "json", theme="monokai",
                   line_numbers=False, word_wrap=True),
            title="Function Response",
            border_style="green",
            padding=(1, 2),
        )

        content = Group(
            *(panel for panel in (call_panel, response_panel) if panel is not None))
        main_panel = Panel(content, title="Tool Invocation",
                           border_style="cyan", padding=1)
        console.print(main_panel)

    def _is_function_call_event(self, obj: Any) -> bool:
        fc = self._extract_function_call(obj)
        return fc is not None

    def _extract_function_call(self, obj: Any) -> Optional[Any]:
        # Common attribute names for function/tool call events
        candidates = (
            "function_call",       # typical
            "tool_call",           # alternative
            "call",                # generic
            "toolInvocation",      # camelCase variants
            "functionCall",
            "toolCall",
        )
        for name in candidates:
            if hasattr(obj, name):
                value = getattr(obj, name)
                if value is not None:
                    return value
        # Some events may represent the call directly as dict-like
        if isinstance(obj, dict):
            if "function_call" in obj and obj["function_call"] is not None:
                return obj["function_call"]
            if "functionCall" in obj and obj["functionCall"] is not None:
                return obj["functionCall"]
        return None

    def _extract_function_response(self, obj: Any) -> Optional[Dict[str, Any]]:
        # Common attribute names for function/tool responses
        candidates = (
            "function_call_response",
            "function_response",
            "function_result",
            "tool_response",
            "tool_output",
            "response",
            "output",
            "result",
        )
        for name in candidates:
            if hasattr(obj, name):
                value = getattr(obj, name)
                if value is not None:
                    return self._coerce_to_dict(value)
        if isinstance(obj, dict):
            for name in candidates:
                if name in obj and obj[name] is not None:
                    return self._coerce_to_dict(obj[name])
        return None

    def _coerce_function_call(self, fc: Any) -> Tuple[str, Dict[str, Any]]:
        # Extract function name
        name_candidates = ("name", "function_name", "tool_name")
        fn_name = None
        if isinstance(fc, dict):
            for k in name_candidates:
                if k in fc and fc[k]:
                    fn_name = str(fc[k])
                    break
        else:
            for k in name_candidates:
                if hasattr(fc, k):
                    v = getattr(fc, k)
                    if v:
                        fn_name = str(v)
                        break
        if not fn_name:
            fn_name = "unknown"

        # Extract args/parameters
        args_candidates = ("args", "arguments", "parameters",
                           "kwargs", "params", "arguments_json")
        args: Dict[str, Any] = {}
        if isinstance(fc, dict):
            for k in args_candidates:
                if k in fc and fc[k] is not None:
                    args = self._coerce_to_dict(fc[k])
                    break
        else:
            for k in args_candidates:
                if hasattr(fc, k):
                    v = getattr(fc, k)
                    if v is not None:
                        args = self._coerce_to_dict(v)
                        break

        return fn_name, args

    def _coerce_to_dict(self, value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            return value
        # Try known conversions
        for attr in ("to_dict", "dict"):
            if hasattr(value, attr) and callable(getattr(value, attr)):
                try:
                    d = getattr(value, attr)()
                    if isinstance(d, dict):
                        return d
                except Exception:
                    pass
        # Dataclass support
        try:
            from dataclasses import asdict, is_dataclass
            if is_dataclass(value):
                return asdict(value)
        except Exception:
            pass
        # Fallback: wrap into a dict
        return {"value": value}

    def _to_pretty_json(self, data: Any) -> str:
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, default=self._json_default)
        except Exception:
            # Last resort
            return json.dumps({"value": str(data)}, ensure_ascii=False, indent=2)

    def _json_default(self, obj: Any) -> Any:
        # Try dict-like conversion for JSON
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            try:
                return obj.to_dict()
            except Exception:
                pass
        try:
            from dataclasses import asdict, is_dataclass
            if is_dataclass(obj):
                return asdict(obj)
        except Exception:
            pass
        try:
            return vars(obj)
        except Exception:
            return str(obj)
