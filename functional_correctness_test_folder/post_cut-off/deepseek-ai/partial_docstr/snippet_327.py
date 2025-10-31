
from typing import Any, Dict
from rich.console import Console


class EventRenderer:

    def __init__(self) -> None:
        self._pending_function_calls: Dict[str, Any] = {}

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if hasattr(obj, 'function_call'):
            self._pending_function_calls[obj.function_call.name] = obj.function_call
        elif hasattr(obj, 'response'):
            for name, response in obj.response.items():
                if name in self._pending_function_calls:
                    self._render_function_call_group(
                        self._pending_function_calls[name], response, console)
                    del self._pending_function_calls[name]

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        for name, function_call in self._pending_function_calls.items():
            console.print(
                f"[bold red]Pending function call: {name}[/bold red]")
        self._pending_function_calls.clear()

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        console.print(
            f"[bold green]Function call: {function_call.name}[/bold green]")
        console.print(
            f"[bold blue]Arguments: {function_call.args}[/bold blue]")
        console.print(f"[bold magenta]Response: {response}[/bold magenta]")
