
from __future__ import annotations

from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import the event types from the ADK event package.
# These imports are optional; if the package is not available the
# renderer will still work for other event types.
try:
    from google.adk.events import FunctionCall, FunctionResponse
except Exception:  # pragma: no cover
    FunctionCall = None  # type: ignore
    FunctionResponse = None  # type: ignore


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        # Store a pending function call until a matching response arrives.
        self._pending_call: Optional[FunctionCall] = None

    def render_event(self, obj: Any, console: Console) -> None:
        """
        Render the provided google.adk.events.Event to rich.console.

        The renderer keeps track of a pending function call. When a
        FunctionCall event is received it is stored. When a
        FunctionResponse event is received it is paired with the
        pending call and rendered together. If a new FunctionCall
        arrives before a response, the previous call is flushed
        without a response.
        """
        # Handle FunctionCall events
        if FunctionCall is not None and isinstance(obj, FunctionCall):
            # Flush any previous pending call before storing the new one
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            self._pending_call = obj
            return

        # Handle FunctionResponse events
        if FunctionResponse is not None and isinstance(obj, FunctionResponse):
            if self._pending_call is None:
                # No pending call – just print the response
                console.print(
                    f"[bold]Function Response:[/bold] {obj.response}",
                    style="green",
                )
            else:
                # Render the call and its response together
                self._render_function_call_group(
                    self._pending_call, obj.response, console
                )
                self._pending_call = None
            return

        # For all other event types, simply print the event
        console.print(obj)

    def _flush_pending_function_call(self, console: Console) -> None:
        """
        Render any pending function call that hasn't been paired with a response.
        """
        if self._pending_call is None:
            return

        # Render the pending call without a response
        console.print(
            Panel(
                f"[bold]Function Call:[/bold] {self._pending_call.function_name}\n"
                f"[dim]{self._pending_call.args or ''}[/dim]",
                title="Unpaired Function Call",
                expand=False,
                style="yellow",
            )
        )
        self._pending_call = None

    def _render_function_call_group(
        self, function_call: FunctionCall, response: dict[str, Any], console: Console
    ) -> None:
        """
        Render function call and response together in a grouped panel.
        """
        # Build a table with two columns: Request and Response
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Request")
        table.add_column("Response")

        # Pretty‑print the request and response payloads
        request_str = (
            f"[bold]{function_call.function_name}[/bold]\n"
            f"{function_call.args or ''}"
        )
        response_str = f"{response}"

        table.add_row(request_str, response_str)

        # Wrap the table in a panel with the function name as the title
        panel = Panel(
            table,
            title=function_call.function_name,
            expand=False,
            style="cyan",
        )
        console.print(panel)
