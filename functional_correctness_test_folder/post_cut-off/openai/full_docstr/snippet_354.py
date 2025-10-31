
from __future__ import annotations

from typing import Any, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import json


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_call: Optional["FunctionCall"] = None

    def render_event(self, obj: "Event", console: Console) -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # Determine event type
        event_type = getattr(obj, "type", None)

        if event_type == "function_call":
            # Store the function call for later pairing
            self._pending_call = getattr(obj, "function_call", None)
        elif event_type == "function_response":
            # Render the pending call with this response
            response = getattr(obj, "response", {})
            if self._pending_call is not None:
                self._render_function_call_group(
                    self._pending_call, response, console
                )
                self._pending_call = None
            else:
                # No pending call; just print the response
                console.print(
                    f"[bold red]Unpaired function response:[/bold red] {response}"
                )
        else:
            # Flush any pending call before rendering other events
            self._flush_pending_function_call(console)
            console.print(obj)

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is not None:
            console.print(
                f"[bold yellow]Unpaired function call:[/bold yellow] {self._pending_call}"
            )
            self._pending_call = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: Dict[str, Any], console: Console
    ) -> None:
        """Render function call and response together in a grouped panel."""
        # Prepare the table with request and response
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="cyan", no_wrap=True)
        table.add_column(style="white")

        # Function call arguments
        args = getattr(function_call, "args", {})
        table.add_row(
            "[bold]Request:[/bold]",
            Text(json.dumps(args, indent=2), style="green"),
        )

        # Function response
        table.add_row(
            "[bold]Response:[/bold]",
            Text(json.dumps(response, indent=2), style="magenta"),
        )

        # Create a panel with the function name as title
        title = getattr(function_call, "name", "Function Call")
        panel = Panel(
            table,
            title=f"[bold]{title}[/bold]",
            border_style="blue",
            expand=False,
        )

        console.print(panel)
