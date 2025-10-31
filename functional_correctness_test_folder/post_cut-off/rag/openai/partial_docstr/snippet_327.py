
from __future__ import annotations

import json
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_call: Optional["FunctionCall"] = None

    def render_event(self, obj: "Event", console: Console) -> None:
        """
        Render the provided google.adk.events.Event to rich.console.

        The renderer keeps track of a pending function call. When a response
        event arrives, it is paired with the pending call and rendered as a
        grouped panel. If a new function call arrives while a previous one
        is still pending, the previous call is flushed without a response.
        """
        # Flush any pending call if a new function call arrives
        if getattr(obj, "function_call", None) is not None:
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            self._pending_call = obj.function_call

        # If a response is present, pair it with the pending call
        if getattr(obj, "response", None) is not None:
            if self._pending_call is not None:
                self._render_function_call_group(
                    self._pending_call, obj.response, console
                )
                self._pending_call = None
            else:
                # No pending call – just render the response alone
                console.print(
                    Panel(
                        Syntax(
                            json.dumps(obj.response, indent=2, sort_keys=True),
                            "json",
                            theme="monokai",
                            line_numbers=False,
                        ),
                        title="Response",
                        border_style="green",
                    )
                )

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is None:
            return

        console.print(
            Panel(
                Syntax(
                    json.dumps(
                        {
                            "name": getattr(self._pending_call, "name", "unknown"),
                            "arguments": getattr(
                                self._pending_call, "arguments", {}
                            ),
                        },
                        indent=2,
                        sort_keys=True,
                    ),
                    "json",
                    theme="monokai",
                    line_numbers=False,
                ),
                title="Function Call (no response)",
                border_style="yellow",
            )
        )
        self._pending_call = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: dict[str, Any], console: Console
    ) -> None:
        """Render function call and response together in a grouped panel."""
        # Prepare the request part
        request_json = json.dumps(
            {
                "name": getattr(function_call, "name", "unknown"),
                "arguments": getattr(function_call, "arguments", {}),
            },
            indent=2,
            sort_keys=True,
        )
        request_syntax = Syntax(
            request_json, "json", theme="monokai", line_numbers=False
        )

        # Prepare the response part
        response_json = json.dumps(response, indent=2, sort_keys=True)
        response_syntax = Syntax(
            response_json, "json", theme="monokai", line_numbers=False
        )

        # Build a table with two columns
        table = Table.grid(expand=True)
        table.add_column(ratio=1)
        table.add_column(ratio=1)
        table.add_row(request_syntax, response_syntax)

        console.print(
            Panel(
                table,
                title=f"Function Call: {getattr(function_call, 'name', 'unknown')}",
                border_style="cyan",
            )
        )
