
from __future__ import annotations

from typing import Any, Dict, List, Optional


class EventRenderer:
    def __init__(self) -> None:
        # Store pending function calls until a response is received
        self._pending_calls: List[Dict[str, Any]] = []

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        """
        Render an event to the console. If the event is a function call,
        store it. If it is a response, flush pending calls and render the
        response.
        """
        if getattr(obj, "type", None) == "function_call":
            # Store the function call event
            self._pending_calls.append(obj.data)
        elif getattr(obj, "type", None) == "response":
            # Flush any pending function calls before rendering the response
            self._flush_pending_function_call(console)
            # Render the response
            console.print(f"[bold green]Response:[/bold green] {obj.data}")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        """
        Flush all pending function calls to the console.
        """
        while self._pending_calls:
            call = self._pending_calls.pop(0)
            # Assume call is a dict with 'function' and 'arguments'
            function_name = call.get("function", "unknown")
            arguments = call.get("arguments", {})
            self._render_function_call_group(function_name, arguments, console)

    def _render_function_call_group(
        self,
        function_name: str,
        arguments: Dict[str, Any],
        console: 'Console',
    ) -> None:
        """
        Render a single function call group to the console.
        """
        console.print(f"[bold cyan]Function Call:[/bold cyan] {function_name}")
        if arguments:
            console.print("[bold]Arguments:[/bold]")
            for key, value in arguments.items():
                console.print(f"  [yellow]{key}[/yellow]: {value}")
        else:
            console.print("  [yellow]No arguments[/yellow]")
