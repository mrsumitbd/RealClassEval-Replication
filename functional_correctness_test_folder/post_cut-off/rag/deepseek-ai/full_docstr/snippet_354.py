
from typing import Any, Dict, Optional
from rich.console import Console


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_function_call: Optional['FunctionCall'] = None

    def render_event(self, obj: 'Event', console: Console) -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        if hasattr(obj, 'function_call'):
            self._pending_function_call = obj.function_call
        elif hasattr(obj, 'response') and self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, obj.response, console)
            self._pending_function_call = None
        elif self._pending_function_call is not None:
            self._flush_pending_function_call(console)

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_function_call is not None:
            console.print(
                f"[bold]Pending Function Call:[/bold] {self._pending_function_call}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: Console) -> None:
        """Render function call and response together in a grouped panel."""
        from rich.panel import Panel
        from rich.text import Text
        content = Text()
        content.append(
            f"[bold]Function Call:[/bold] {function_call}\n", style="green")
        content.append(f"[bold]Response:[/bold] {response}", style="blue")
        console.print(
            Panel(content, title="Function Call Group", border_style="yellow"))
