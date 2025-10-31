
from __future__ import annotations

import json
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_call: Optional[Any] = None
        self._pending_response: Optional[dict[str, Any]] = None

    def render_event(self, obj: "Event", console: "Console") -> None:
        """
        Render an event. If the event is a function call or a function response,
        it will be grouped together. Other events are printed immediately.
        """
        # Detect a function call
        if hasattr(obj, "function_call"):
            # Flush any previous pending call without a response
            self._flush_pending_function_call(console)
            self._pending_call = obj.function_call
            # If a response already exists, flush immediately
            if self._pending_response is not None:
                self._flush_pending_function_call(console)
            return

        # Detect a function response
        if hasattr(obj, "function_response"):
            self._pending_response = obj.function_response
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            return

        # For all other events, flush any pending call and print the event
        self._flush_pending_function_call(console)
        console.print(obj)

    def _flush_pending_function_call(self, console: "Console") -> None:
        """Flush the pending function call (and its response if available)."""
        if self._pending_call is None:
            return

        if self._pending_response is not None:
            self._render_function_call_group(
                self._pending_call, self._pending_response, console
            )
        else:
            # No response yet; just print the call
            console.print(self._pending_call)

        # Reset pending state
        self._pending_call = None
        self._pending_response = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: dict[str, Any], console: "Console"
    ) -> None:
        """Render function call and response together in a grouped panel."""
        # Prepare a table with two columns: Call and Response
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Call", style="cyan", no_wrap=True)
        table.add_column("Response", style="green")

        # Convert function call to a readable string
        try:
            call_str = f"{function_call.name}({function_call.arguments})"
        except Exception:
            call_str = str(function_call)

        # Convert response dict to pretty JSON
        try:
            response_str = json.dumps(response, indent=2, default=str)
        except Exception:
            response_str = str(response)

        table.add_row(call_str, response_str)

        # Create a panel with the function name as title
        title = getattr(function_call, "name", "Function Call")
        panel = Panel(table, title=title, expand=False, border_style="blue")

        console.print(panel)
