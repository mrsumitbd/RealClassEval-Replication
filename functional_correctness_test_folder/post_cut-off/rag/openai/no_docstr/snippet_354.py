
from __future__ import annotations

from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_call: Optional["FunctionCall"] = None

    def render_event(self, obj: "Event", console: Console) -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # If the event is a function call, store it as pending
        if getattr(obj, "type", None) == "function_call":
            # Flush any previous pending call before storing new one
            self._flush_pending_function_call(console)
            self._pending_call = obj.function_call
            return

        # If the event is a function response, try to pair with pending call
        if getattr(obj, "type", None) == "function_response":
            if self._pending_call is not None:
                self._render_function_call_group(
                    self._pending_call, obj.response, console
                )
                self._pending_call = None
            else:
                # No pending call; just render the response alone
                console.print(
                    Panel(
                        Text.from_markup(
                            f"[bold]Function Response:[/bold] {obj.response}"
                        ),
                        title="Function Response",
                    )
                )
            return

        # For any other event type, flush pending call and render normally
        self._flush_pending_function_call(console)
        console.print(obj)

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is not None:
            console.print(
                Panel(
                    Text.from_markup(
                        f"[bold]Unpaired Function Call:[/bold] {self._pending_call}"
                    ),
                    title="Function Call",
                )
            )
            self._pending_call = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: dict[str, Any], console: Console
    ) -> None:
        """Render function call and response together in a grouped panel."""
        table = Table.grid(padding=1)
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="magenta")

        # Render function call details
        table.add_row("[bold]Function Call[/bold]", str(function_call))

        # Render response details
        table.add_row("[bold]Response[/bold]", str(response))

        console.print(Panel(table, title="Function Call Group", expand=False))
