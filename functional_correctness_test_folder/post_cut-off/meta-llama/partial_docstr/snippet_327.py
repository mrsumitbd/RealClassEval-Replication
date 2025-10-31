
from rich.console import Console
from typing import Any


class Event:
    pass  # Assuming Event class is defined elsewhere


class FunctionCall:
    pass  # Assuming FunctionCall class is defined elsewhere


class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if hasattr(obj, 'function_call'):
            if self.pending_function_call is not None:
                self._flush_pending_function_call(console)
            self.pending_function_call = obj
        elif hasattr(obj, 'response'):
            if self.pending_function_call is not None:
                self._render_function_call_group(
                    self.pending_function_call, obj.response, console)
                self.pending_function_call = None
            else:
                console.print(
                    "[bold red]Unexpected response without a function call[/bold red]")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        console.print("[bold red]Function call without a response[/bold red]")
        console.print(self.pending_function_call)
        self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        console.print("[bold]Function Call:[/bold]")
        console.print(function_call)
        console.print("[bold]Response:[/bold]")
        console.print(response)
