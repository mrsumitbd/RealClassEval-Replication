
from typing import Any
from rich.console import Console
from .events import Event, FunctionCall


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call: FunctionCall | None = None

    def render_event(self, obj: Event, console: Console) -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        if isinstance(obj, FunctionCall):
            self._flush_pending_function_call(console)
            self._pending_function_call = obj
        else:
            if self._pending_function_call is not None:
                if obj.get('id') == self._pending_function_call.id:
                    self._render_function_call_group(
                        self._pending_function_call, obj, console)
                    self._pending_function_call = None
                else:
                    self._flush_pending_function_call(console)
                    console.print(obj)
            else:
                console.print(obj)

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is not None:
            console.print(self._pending_function_call)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: FunctionCall, response: dict[str, Any], console: Console) -> None:
        """Render function call and response together in a grouped panel."""
        from rich.panel import Panel
        from rich.text import Text
        text = Text.assemble(
            Text(f"Function Call: {function_call.name}\n", style="bold"),
            Text(f"ID: {function_call.id}\n"),
            Text(f"Params: {function_call.params}\n"),
            Text("\n"),
            Text("Response:\n", style="bold"),
            Text(str(response)),
        )
        console.print(Panel(text, title="RPC Call"))
