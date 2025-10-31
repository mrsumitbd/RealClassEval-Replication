
from typing import Any, Optional


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None
        self._pending_response: Optional[dict[str, Any]] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # Assume Event has .type and .data
        if obj.type == "function_call":
            # If there is a pending function call, flush it first
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.data
            self._pending_response = None
        elif obj.type == "function_response":
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.data, console)
                self._pending_function_call = None
                self._pending_response = None
            else:
                # No pending function call, just print the response
                console.print(
                    f"[bold yellow]Unpaired function response:[/bold yellow] {obj.data}")
        else:
            # For other event types, flush any pending function call and print the event
            self._flush_pending_function_call(console)
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            console.print(
                f"[bold cyan]Function call (no response):[/bold cyan] {self._pending_function_call}")
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.table import Table

        table = Table.grid(padding=(0, 1))
        table.add_row("[bold]Function Call[/bold]", str(function_call))
        table.add_row("[bold]Response[/bold]", str(response))
        panel = Panel(table, title="Function Call & Response",
                      border_style="green")
        console.print(panel)
