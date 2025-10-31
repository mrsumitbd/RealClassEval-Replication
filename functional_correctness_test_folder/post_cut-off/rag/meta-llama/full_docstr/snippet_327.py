
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
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
        elif self._pending_function_call is not None:
            if obj.correlation_id == self._pending_function_call.correlation_id:
                self._render_function_call_group(
                    self._pending_function_call, obj.__dict__, console)
                self._pending_function_call = None
            else:
                self._flush_pending_function_call(console)
                console.print(obj.__dict__)
        else:
            console.print(obj.__dict__)

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, {}, console)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: FunctionCall, response: dict[str, Any], console: Console) -> None:
        """Render function call and response together in a grouped panel."""
        title = Text(f"Function Call: {function_call.name}")
        if response:
            content = Text.assemble(
                ("Request:\n", "bold"),
                str(function_call.__dict__),
                ("\nResponse:\n", "bold"),
                str(response),
            )
        else:
            content = Text.assemble(
                ("Request:\n", "bold"),
                str(function_call.__dict__),
                ("\nResponse: Pending", "bold red"),
            )
        console.print(Panel(content, title=title))
