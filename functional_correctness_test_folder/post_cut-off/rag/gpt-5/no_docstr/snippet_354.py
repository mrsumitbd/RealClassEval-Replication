from typing import Any, Optional, Dict


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        function_call = self._extract_function_call(obj)
        if function_call is not None:
            # If we already had a pending call that never got a response, flush it.
            self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        response = self._extract_function_response(obj)
        if response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, response, console)
                self._pending_function_call = None
            else:
                self._render_response_only(response, console)
            return

        # Not a function call nor a response; flush pending and print event as-is.
        self._flush_pending_function_call(console)
        self._render_generic_event(obj, console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is None:
            return
        self._render_call_only(self._pending_function_call, console)
        self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.pretty import Pretty
        from rich.text import Text
        from rich.console import Group

        name, args = self._normalize_function_call(function_call)
        header = Text(f"Function: {name}", style="bold cyan") if name else Text(
            "Function Call", style="bold cyan")
        body = Group(
            Text("Arguments", style="bold"),
            Pretty(args, expand_all=True),
            Text("Response", style="bold green"),
            Pretty(response, expand_all=True),
        )
        console.print(Panel(body, title=header, border_style="cyan"))

    # Helper rendering methods

    def _render_call_only(self, function_call: Any, console: 'Console') -> None:
        from rich.panel import Panel
        from rich.pretty import Pretty
        from rich.text import Text
        from rich.console import Group

        name, args = self._normalize_function_call(function_call)
        header = Text(f"Function: {name}", style="bold yellow") if name else Text(
            "Function Call (unpaired)", style="bold yellow")
        body = Group(
            Text("Arguments", style="bold"),
            Pretty(args, expand_all=True),
        )
        console.print(Panel(body, title=header, border_style="yellow"))

    def _render_response_only(self, response: Dict[str, Any], console: 'Console') -> None:
        from rich.panel import Panel
        from rich.pretty import Pretty
        from rich.text import Text

        console.print(Panel(Pretty(response, expand_all=True), title=Text(
            "Function Response (unpaired)", style="bold green"), border_style="green"))

    def _render_generic_event(self, obj: Any, console: 'Console') -> None:
        try:
            from rich.pretty import Pretty
            console.print(Pretty(obj, expand_all=True))
        except Exception:
            console.print(obj)

    # Extraction and normalization helpers

    def _extract_function_call(self, event: Any) -> Optional[Any]:
        # Direct attribute
        if hasattr(event, "function_call"):
            return getattr(event, "function_call")

        # Common dict structures
        if isinstance(event, dict):
            if "function_call" in event:
                return event["function_call"]
            if event.get("type") in {"function_call", "tool_call"}:
                payload = event.get("data") or event.get(
                    "payload") or event.get("function_call")
                if payload is not None:
                    return payload

        # Nested data attribute
        data = getattr(event, "data", None)
        if isinstance(data, dict) and "function_call" in data:
            return data["function_call"]

        return None

    def _extract_function_response(self, event: Any) -> Optional[Dict[str, Any]]:
        # Direct attribute
        if hasattr(event, "function_response"):
            return self._to_dict(getattr(event, "function_response"))

        # Common dict structures
        if isinstance(event, dict):
            for key in ("function_response", "response", "tool_result", "function_result", "function_output", "output"):
                if key in event and event[key] is not None:
                    return self._to_dict(event[key])
            if event.get("type") in {"function_response", "tool_result", "function_result"}:
                payload = event.get("data") or event.get(
                    "payload") or event.get("response")
                if payload is not None:
                    return self._to_dict(payload)

        # Nested data attribute
        data = getattr(event, "data", None)
        if isinstance(data, dict):
            for key in ("function_response", "response", "tool_result", "function_result", "function_output", "output"):
                if key in data and data[key] is not None:
                    return self._to_dict(data[key])

        return None

    def _normalize_function_call(self, call: Any) -> tuple[Optional[str], Any]:
        # Extract name
        name = None
        if isinstance(call, dict):
            name = call.get("name") or call.get("function") or call.get("id")
        else:
            for attr in ("name", "function", "id"):
                if hasattr(call, attr):
                    name = getattr(call, attr)
                    break

        # Extract arguments
        args: Any = None
        if isinstance(call, dict):
            for key in ("arguments", "args", "parameters", "params", "input", "inputs"):
                if key in call and call[key] is not None:
                    args = call[key]
                    break
            if args is None:
                # Fallback to everything except likely metadata keys
                args = {k: v for k, v in call.items() if k not in {
                    "name", "function", "id", "type"}}
        else:
            for attr in ("arguments", "args", "parameters", "params", "input", "inputs"):
                if hasattr(call, attr):
                    args = getattr(call, attr)
                    break
            if args is None:
                # Fallback to object's __dict__
                args = getattr(call, "__dict__", call)

        return name, args

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            try:
                return dict(obj.to_dict())
            except Exception:
                pass
        if hasattr(obj, "__dict__"):
            try:
                return dict(obj.__dict__)
            except Exception:
                pass
        # As a last resort, wrap in a dict
        return {"value": obj}
