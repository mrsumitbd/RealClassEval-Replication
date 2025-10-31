
from __future__ import annotations

from typing import Any, Optional

# The imports below are intentionally local to avoid importing heavy modules
# unless the methods are actually called.
# They are imported inside the methods that need them.


class EventRenderer:
    """Stateful renderer that groups function calls with their responses."""

    def __init__(self) -> None:
        """Initialize the event renderer."""
        # Holds the most recent function call that hasn't yet been paired
        # with a response.  It is expected to be an object that has an
        # ``id`` attribute (or ``call_id``) that can be matched against
        # the response's ``id``.
        self._pending_call: Optional[Any] = None

    def render_event(self, obj: "Event", console: "Console") -> None:
        """
        Render the provided google.adk.events.Event to rich.console.

        The renderer keeps track of the most recent function call that
        hasn't yet been paired with a response.  When a response event
        arrives that matches the pending call, the two are rendered
        together in a grouped panel.  If a new function call arrives
        while a previous one is still pending, the previous one is
        flushed (rendered without a response) before the new one is
        stored.
        """
        # Import here to keep the module lightweight.
        from rich.console import Console

        # Detect a function call event.  The exact attribute names may
        # vary; we try a few common ones.
        function_call = None
        if hasattr(obj, "function_call"):
            function_call = getattr(obj, "function_call")
        elif hasattr(obj, "call"):
            function_call = getattr(obj, "call")

        # Detect a response event.  Again, we try a few common names.
        response = None
        if hasattr(obj, "response"):
            response = getattr(obj, "response")
        elif hasattr(obj, "result"):
            response = getattr(obj, "result")

        # If this is a function call event.
        if function_call is not None:
            # Flush any previously pending call.
            if self._pending_call is not None:
                self._flush_pending_function_call(console)
            # Store the new pending call.
            self._pending_call = function_call
            return

        # If this is a response event.
        if response is not None:
            # Try to match the response to the pending call.
            pending_id = None
            if self._pending_call is not None:
                pending_id = getattr(self._pending_call, "id", None) or getattr(
                    self._pending_call, "call_id", None
                )
            response_id = getattr(response, "id", None) or getattr(
                response, "call_id", None
            )

            if pending_id is not None and pending_id == response_id:
                # We have a match – render the group.
                self._render_function_call_group(
                    self._pending_call, response, console
                )
                self._pending_call = None
            else:
                # No match – flush any pending call first.
                if self._pending_call is not None:
                    self._flush_pending_function_call(console)
                # Render the response on its own.
                console.print(
                    f"[bold]Response:[/bold] {self._format_value(response)}"
                )
            return

        # If the event is neither a function call nor a response,
        # just print it directly.
        console.print(self._format_value(obj))

    def _flush_pending_function_call(self, console: "Console") -> None:
        """
        Render any pending function call that hasn't been paired with a
        response.
        """
        if self._pending_call is None:
            return
        console.print(
            f"[bold]Function call (unpaired):[/bold] {self._format_value(self._pending_call)}"
        )
        self._pending_call = None

    def _render_function_call_group(
        self, function_call: Any, response: dict[str, Any], console: "Console"
    ) -> None:
        """
        Render function call and response together in a grouped panel.
        """
        from rich.panel import Panel
        from rich.table import Table
        from rich.pretty import Pretty

        table = Table.grid(padding=1)
        table.add_column(justify="right", style="bold cyan")
        table.add_column()

        table.add_row("Function Call:", Pretty(function_call))
        table.add_row("Response:", Pretty(response))

        panel = Panel(
            table,
            title="Function Call Group",
            expand=False,
            border_style="green",
        )
        console.print(panel)

    @staticmethod
    def _format_value(value: Any) -> str:
        """
        Helper to convert a value to a string suitable for printing.
        """
        try:
            from rich.pretty import Pretty

            return str(Pretty(value))
        except Exception:
            return str(value)
