
from __future__ import annotations

from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table


class EventRenderer:
    """
    Render Google ADK events to a Rich console.

    The renderer keeps track of pending function calls and renders them
    together with their responses when available.  If a response is not
    received, the pending call is flushed at the end.
    """

    def __init__(self) -> None:
        # Store pending function calls until a response arrives.
        self._pending_calls: List[Any] = []

    def render_event(self, obj: "Event", console: "Console") -> None:
        """
        Render the provided google.adk.events.Event to rich.console.

        Parameters
        ----------
        obj : Event
            The event to render.  It may be a function call or a function
            response.
        console : Console
            The Rich console to write to.
        """
        # Detect a function call: it should have a `function_name` attribute.
        if hasattr(obj, "function_name"):
            self._pending_calls.append(obj)
            return

        # Detect a function response: it should have a `response` attribute.
        if hasattr(obj, "response"):
            # Find the earliest pending call that matches the function name.
            # If no match is found, we simply ignore the response.
            matched_call: Optional[Any] = None
            for i, call in enumerate(self._pending_calls):
                if getattr(call, "function_name", None) == getattr(obj, "function_name", None):
                    matched_call = call
                    del self._pending_calls[i]
                    break

            if matched_call is not None:
                self._render_function_call_group(
                    matched_call, getattr(obj, "response", {}), console
                )
            else:
                # No matching call; render the response alone.
                self._render_function_call_group(
                    None, getattr(obj, "response", {}), console)
            return

        # For any other event type, just print its representation.
        console.print(f"[italic]Event:[/italic] {repr(obj)}")

    def _flush_pending_function_call(self, console: "Console") -> None:
        """
        Render any pending function call that hasn't been paired with a response.
        """
        while self._pending_calls:
            call = self._pending_calls.pop(0)
            self._render_function_call_group(call, None, console)

    def _render_function_call_group(
        self,
        function_call: Optional["FunctionCall"],
        response: Optional[Dict[str, Any]],
        console: "Console",
    ) -> None:
        """
        Render a function call and its response as a table.

        Parameters
        ----------
        function_call : FunctionCall | None
            The function call object.  If None, the table will only show the
            response.
        response : dict[str, Any] | None
            The response data.  If None, the response column will show
            "[bold]Pending[/bold]".
        console : Console
            The Rich console to write to.
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Details", style="white")

        if function_call is not None:
            fn_name = getattr(function_call, "function_name", "<unknown>")
            args = getattr(function_call, "arguments", {})
            table.add_row("[bold]Function[/bold]", f"{fn_name}")
            table.add_row("[bold]Arguments[/bold]", f"{args!r}")
        else:
            table.add_row("[bold]Function[/bold]", "[italic]None[/italic]")

        if response is not None:
            table.add_row("[bold]Response[/bold]", f"{response!r}")
        else:
            table.add_row("[bold]Response[/bold]", "[bold]Pending[/bold]")

        console.print(table)
