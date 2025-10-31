
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        if isinstance(obj, FunctionCall):
            self._flush_pending_function_call(console)
            self._pending_function_call = obj
        elif isinstance(obj, FunctionCallResponse):
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.response, console)
                self._pending_function_call = None
            else:
                console.print(
                    Panel(Text("Unexpected response"), title="Response"))
        else:
            console.print(Panel(Text(str(obj)), title="Event"))

    def _flush_pending_function_call(self, console: 'Console') -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, {}, console)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        """Render function call and response together in a grouped panel."""
        title = f"{function_call.name} ({function_call.id})"
        function_call_text = Text(function_call.name + "(")
        for i, arg in enumerate(function_call.args):
            if i > 0:
                function_call_text.append(", ")
            function_call_text.append(str(arg))
        function_call_text.append(")")
        response_text = Text(str(response))
        panel = Panel.fit(function_call_text, title="Call")
        console.print(panel)
        if response:
            panel = Panel.fit(response_text, title="Response")
            console.print(panel)
