
from typing import Any, Optional


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # Assume Event has .type and .data
        if getattr(obj, 'type', None) == 'function_call':
            # If there is a pending function call, flush it first
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.data  # Assume .data is a FunctionCall
        elif getattr(obj, 'type', None) == 'function_response':
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.data, console)
                self._pending_function_call = None
            else:
                # No pending function call, just print the response
                console.print(
                    f"[bold yellow]Unpaired function response:[/bold yellow] {obj.data}")
        else:
            # For other event types, flush pending and print event
            self._flush_pending_function_call(console)
            console.print(f"[bold cyan]Event:[/bold cyan] {obj}")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            console.print(
                f"[bold magenta]Unpaired function call:[/bold magenta] {self._pending_function_call}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.table import Table

        table = Table.grid(padding=(0, 1))
        table.add_row("[bold green]Function Call[/bold green]:",
                      str(function_call))
        table.add_row("[bold blue]Response[/bold blue]:", str(response))
        panel = Panel(table, title="Function Call Group", border_style="green")
        console.print(panel)
