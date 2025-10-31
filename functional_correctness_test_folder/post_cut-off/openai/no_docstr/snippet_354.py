
from __future__ import annotations

from typing import Any, List, Dict

# The following imports are optional; they are used only if the
# corresponding classes are available in the runtime environment.
try:
    from rich.console import Console
except Exception:  # pragma: no cover
    Console = None  # type: ignore


class EventRenderer:
    """
    A simple renderer that collects function call events and renders them
    together with their corresponding responses to a Rich console.
    """

    def __init__(self) -> None:
        # Store pending function calls until a response is received.
        self._pending_calls: List["FunctionCall"] = []

    def render_event(self, obj: "Event", console: "Console") -> None:
        """
        Render an event. If the event is a function call, it is queued.
        If the event is a response, all queued function calls are rendered
        with the response data.
        """
        # Basic type checks to avoid attribute errors.
        if not hasattr(obj, "type") or not hasattr(obj, "data"):
            return

        event_type = getattr(obj, "type")
        data = getattr(obj, "data")

        if event_type == "function_call":
            # Queue the function call for later rendering.
            self._pending_calls.append(data)
        elif event_type == "response":
            # Render all pending function calls with this response.
            self._flush_pending_function_call(console)
        else:
            # For any other event type, just print its data.
            console.print(f"[bold]{event_type}[/bold]: {data}")

    def _flush_pending_function_call(self, console: "Console") -> None:
        """
        Render all pending function calls with the most recent response.
        """
        # If there are no pending calls, nothing to do.
        if not self._pending_calls:
            return

        # In a real implementation, the response would be passed from
        # the caller. Here we assume the last event was a response and
        # that the response data is available as a global variable.
        # For safety, we use an empty dict if no response is available.
        response: Dict[str, Any] = getattr(console, "_last_response", {})

        for function_call in self._pending_calls:
            self._render_function_call_group(function_call, response, console)

        # Clear the queue after rendering.
        self._pending_calls.clear()

    def _render_function_call_group(
        self, function_call: "FunctionCall", response: Dict[str, Any], console: "Console"
    ) -> None:
        """
        Render a single function call and its response.
        """
        # Extract function name and arguments.
        name = getattr(function_call, "name", "<unknown>")
        args = getattr(function_call, "arguments", {})
        kwargs = getattr(function_call, "kwargs", {})

        # Print the function call.
        console.print(f"[green]Function Call:[/green] {name}")
        if args:
            console.print(f"  [cyan]Args:[/cyan] {args}")
        if kwargs:
            console.print(f"  [cyan]Kwargs:[/cyan] {kwargs}")

        # Print the response.
        if response:
            console.print(f"[magenta]Response:[/magenta] {response}")
        else:
            console.print("[magenta]No response available[/magenta]")
