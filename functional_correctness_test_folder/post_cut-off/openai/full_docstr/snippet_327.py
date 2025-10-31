
from __future__ import annotations

from typing import Any, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        self._pending_call: Optional[FunctionCall] = None
        self._pending_response: Optional[Dict[str, Any]] = None

    def render_event(self, obj: "Event", console: Console) -> None:
        """Render the provided google.adk.events.Event to rich.console."""
        # Detect function call
        if hasattr(obj, "function_call") and obj.function_call is not None:
            # If we already have a pending call, flush it first
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            self._pending_call = obj.function_call
            self._pending_response = None
            return

        # Detect function response
        if hasattr(obj, "function_response") and obj.function_response is not None:
            if self._pending_call is not None:
                # Pair with the pending call
                self._render_function_call_group(
                    self._pending_call, obj.function_response, console
                )
                self._pending_call = None
                self._pending_response = None
            else:
                # No pending call; just render the response alone
                console.print(
                    Panel(
                        Text.from_markup(
                            f"[bold]Function Response:[/bold]\n{obj.function_response}"
                        ),
                        title="Function Response",
                        border_style="yellow",
                    )
                )
            return

        # Default rendering for other event types
        if hasattr(obj, "message") and obj.message is not None:
            console.print(obj.message)
        else:
            console.print(f"[italic]Unrecognized event: {obj!r}[/italic]")

    def _flush_pending_function_call(self, console: Console) -> None:
        """Render any pending function call that hasn't been paired with a response."""
        if self._pending_call is not None:
            console.print(
                Panel(
                    Text.from_markup(
                        f"[bold]Function Call:[/bold]\n{self._pending_call}"
                    ),
                    title="Function Call",
                    border_style="cyan",
                )
            )
            self._pending_call = None
            self._pending_response = None

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: Dict[str, Any], console: Console
    ) -> None:
        """Render function call and response together in a grouped panel."""
        table = Table.grid(padding=1)
        table.add_column(justify="right", style="bold magenta")
        table.add_column(style="white")

        # Arguments
        args_text = Text.from_markup(str(function_call.arguments))
        table.add_row("Arguments:", args_text)

        # Response
        resp_text = Text.from_markup(str(response))
        table.add_row("Response:", resp_text)

        console.print(
            Panel(
                table,
                title=f"[bold]{function_call.name}[/bold]",
                border_style="green",
            )
        )
