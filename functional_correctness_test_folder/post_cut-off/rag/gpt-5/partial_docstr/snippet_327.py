from typing import Any, Optional
import json

from rich.console import Group
from rich.panel import Panel
from rich.pretty import Pretty
from rich.rule import Rule
from rich.text import Text


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[Any] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # Attempt to extract function call and response from event
        function_call = getattr(obj, "function_call", None)
        function_response = (
            getattr(obj, "function_call_response", None)
            if not hasattr(obj, "function_response")
            else getattr(obj, "function_response")
        )
        if function_response is None:
            # Some events might use "response" for function responses
            resp_attr = getattr(obj, "response", None)
            if isinstance(resp_attr, dict) or isinstance(resp_attr, str):
                function_response = resp_attr

        # If event contains both call and response, render together immediately
        if function_call is not None and function_response is not None:
            self._flush_pending_function_call(console)
            self._render_function_call_group(
                function_call, function_response, console)
            return

        # If event contains a function call, set it as pending
        if function_call is not None:
            # If a previous call is still pending, flush it before setting a new one
            self._flush_pending_function_call(console)
            self._pending_function_call = function_call
            return

        # If event contains a function response, render it with pending call if available
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

        # For any other event types, flush pending call and then render the event plainly
        self._flush_pending_function_call(console)
        console.print(Pretty(obj))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            self._render_function_call_group(self._pending_function_call, {
                                             "status": "no response yet"}, console)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        def _to_jsonish(value: Any) -> Any:
            if isinstance(value, (str, bytes)):
                try:
                    return json.loads(value)
                except Exception:
                    return value
            return value

        def _call_info(fc: Any) -> dict[str, Any]:
            if fc is None:
                return {"name": "(unknown)", "arguments": {}}
            name = getattr(fc, "name", None) or getattr(
                fc, "function", None) or type(fc).__name__
            # Prefer "arguments", then "args"/"kwargs"
            arguments = getattr(fc, "arguments", None)
            if arguments is None:
                args = getattr(fc, "args", None)
                kwargs = getattr(fc, "kwargs", None)
                if args is not None or kwargs is not None:
                    arguments = {"args": args, "kwargs": kwargs}
            arguments = _to_jsonish(arguments) if arguments is not None else {}
            return {"name": name, "arguments": arguments}

        call_data = _call_info(function_call)
        response_data = _to_jsonish(response)

        call_header = Text("Function Call", style="bold")
        call_name = Text(f"Name: {call_data['name']}", style="bold cyan")
        call_args = Pretty(call_data["arguments"])

        resp_header = Text("Response", style="bold")
        resp_body = Pretty(response_data)

        group = Group(
            call_header,
            call_name,
            call_args,
            Rule(),
            resp_header,
            resp_body,
        )
        console.print(Panel(group, title="Function Interaction", expand=False))
