
from __future__ import annotations

import json
from typing import Any, Dict, Optional

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
        # Determine event type.  The exact attribute names depend on the
        # google.adk.events.Event implementation, but we assume the following
        # common interface:
        #
        #   obj.type: str  # e.g. "function_call" or "response"
        #   obj.function_call: FunctionCall (for function_call events)
        #   obj.response: dict (for response events)
        #
        # If the event is a function call, we store it as pending.  If a
        # response arrives, we pair it with the pending call and render
        # them together.  If a new function call arrives while a previous
        # one is still pending, we flush the previous one first.
        #
        # If a response arrives with no pending call, we simply render it
        # as a standalone panel.

        event_type = getattr(obj, "type", None)

        if event_type == "function_call":
            # Flush any previous pending call before storing the new one.
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            self._pending_call = getattr(obj, "function_call", None)

        elif event_type == "response":
            # Render the response with the pending call if available.
            if self._pending_call is not None:
                response_data = getattr(obj, "response", {})
                self._render_function_call_group(
                    self._pending_call, response_data, console)
                self._pending_call = None
            else:
                # No pending call; render the response alone.
                response_data = getattr(obj, "response", {})
                self._render_response_only(response_data, console)

        else:
            # Unknown event type; ignore or render raw representation.
            console.print(
                f"[yellow]Unknown event type: {event_type!r}[/yellow]")

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is not None:
            # Render the function call without a response.
            self._render_function_call_group(self._pending_call, {}, console)
            self._pending_call = None

    def _render_function_call_group(
        self,
        function_call: "FunctionCall",
        response: Dict[str, Any],
        console: Console,
    ) -> None:
        """Render function call and response together in a grouped panel."""
        # Build a table with two columns: Request and Response.
        table = Table.grid(expand=True)
        table.add_column(justify="right", style="bold cyan")
        table.add_column(justify="left", style="white")

        # Function call details.
        func_name = getattr(function_call, "name", "<unknown>")
        func_args = getattr(function_call, "arguments", {})
        table.add_row("Function:", func_name)
        table.add_row("Arguments:", json.dumps(func_args, indent=2))

        # Response details.
        if response:
            table.add_row("Response:", json.dumps(response, indent=2))
        else:
            table.add_row("Response:", "[italic]No response yet[/italic]")

        panel_title = f"[bold green]Function Call: {func_name}[/bold green]"
        panel = Panel(table, title=panel_title,
                      expand=False, border_style="green")
        console.print(panel)

    def _render_response_only(self, response: Dict[str, Any], console: Console) -> None:
        """Render a response that has no matching function call."""
        table = Table.grid(expand=True)
        table.add_column(justify="right", style="bold magenta")
        table.add_column(justify="left", style="white")
        table.add_row("Response:", json.dumps(response, indent=2))
        panel = Panel(
            table, title="[bold magenta]Unpaired Response[/bold magenta]", expand=False, border_style="magenta")
        console.print(panel)
