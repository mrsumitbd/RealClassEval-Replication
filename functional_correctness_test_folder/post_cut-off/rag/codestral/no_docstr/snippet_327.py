
from typing import Any, Dict, Optional
from rich.console import Console
from google.adk.events import Event, FunctionCall


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[FunctionCall] = None

    def render_event(self, obj: Event, console: Console) -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if isinstance(obj, FunctionCall):
            self._flush_pending_function_call(console)
            self._pending_function_call = obj
        elif self._pending_function_call is not None and hasattr(obj, 'response'):
            self._render_function_call_group(
                self._pending_function_call, obj.response, console)
            self._pending_function_call = None

    def _flush_pending_function_call(self, console: Console) -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            console.print(
                f"[bold]Function Call:[/bold] {self._pending_function_call.name}")
            console.print(
                f"[bold]Arguments:[/bold] {self._pending_function_call.arguments}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: FunctionCall, response: Dict[str, Any], console: Console) -> None:
        '''Render function call and response together in a grouped panel.'''
        console.print("[bold]Function Call:[/bold]")
        console.print(f"Name: {function_call.name}")
        console.print(f"Arguments: {function_call.arguments}")
        console.print("\n[bold]Response:[/bold]")
        for key, value in response.items():
            console.print(f"{key}: {value}")
