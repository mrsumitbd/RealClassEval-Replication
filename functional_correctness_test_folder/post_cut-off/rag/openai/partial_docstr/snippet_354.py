
from __future__ import annotations

from typing import Any, Optional

# Rich imports – these are optional and only used when rendering.
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except Exception:  # pragma: no cover
    Console = None  # type: ignore
    Panel = None  # type: ignore
    Table = None  # type: ignore


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        # Store a pending function call until a matching response arrives.
        self._pending_call: Optional[Any] = None

    def render_event(self, obj: "Event", console: "Console") -> None:
        """
        Render the provided google.adk.events.Event to rich.console.

        The renderer keeps track of a pending function call. When a response
        event arrives, the call and response are rendered together in a
        grouped panel. If a new function call arrives before a response,
        the previous call is flushed as a standalone entry.
        """
        # Detect a function call event.
        if hasattr(obj, "function_call") and getattr(obj, "function_call") is not None:
            # Flush any previous pending call before storing the new one.
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            self._pending_call = getattr(obj, "function_call")

        # Detect a response event.
        if hasattr(obj, "response") and getattr(obj, "response") is not None:
            response = getattr(obj, "response")
            if self._pending_call is not None:
                # Render the call and its response together.
                self._render_function_call_group(
                    self._pending_call, response, console)
                self._pending_call = None
            else:
                # No pending call – just print the response.
                console.print(f"[bold]Response:[/bold] {response}")

        # If the event is neither a call nor a response, just print it.
        if not (
            (hasattr(obj, "function_call") and getattr(
                obj, "function_call") is not None)
            or (hasattr(obj, "response") and getattr(obj, "response") is not None)
        ):
            console.print(obj)

    def _flush_pending_function_call(self, console: "Console") -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is not None:
            console.print(f"[bold]Function Call:[/bold] {self._pending_call}")
            self._pending_call = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: dict[str, Any], console: "Console"
    ) -> None:
        """Render function call and response together in a grouped panel."""
        # Build a simple two‑column table: one for the call, one for the response.
        table = Table.grid(padding=1)
        table.add_column(justify="right")
        table.add_column()
        table.add_row("[bold]Function Call[/bold]", str(function_call))
        table.add_row("[bold]Response[/bold]", str(response))

        # Wrap the table in a panel for visual grouping.
        panel = Panel(table, title="Function Call Group", expand=False)
        console.print(panel)
