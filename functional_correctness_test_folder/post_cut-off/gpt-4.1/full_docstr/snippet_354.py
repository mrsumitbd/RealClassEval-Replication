
from typing import Any, Optional


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if hasattr(obj, "function_call") and obj.function_call is not None:
            # If there is a pending function call, flush it first
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.function_call
        elif hasattr(obj, "function_response") and obj.function_response is not None:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.function_response, console)
                self._pending_function_call = None
            else:
                # No pending function call, just render the response
                console.print(
                    f"[bold yellow]Function Response:[/bold yellow] {obj.function_response}")
        else:
            # Render other event types directly
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            console.print(
                f"[bold cyan]Function Call (no response):[/bold cyan] {self._pending_function_call}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.table import Table

        table = Table.grid(padding=(0, 1))
        table.add_row("[bold cyan]Function Call[/bold cyan]",
                      str(function_call))
        table.add_row("[bold green]Response[/bold green]", str(response))
        panel = Panel(table, title="Function Call & Response",
                      border_style="magenta")
        console.print(panel)
