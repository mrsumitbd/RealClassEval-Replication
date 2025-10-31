
from typing import Any, Optional, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        # If the event is a function call, store it as pending
        if hasattr(obj, "function_call"):
            # If there is already a pending function call, flush it first
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.function_call
        # If the event is a function response, pair it with the pending function call
        elif hasattr(obj, "function_response"):
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj.function_response, console)
                self._pending_function_call = None
            else:
                # No pending function call, just render the response
                self._render_function_call_group(
                    None, obj.function_response, console)
        else:
            # For other event types, flush any pending function call and render the event as is
            self._flush_pending_function_call(console)
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call, None, console)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: Optional['FunctionCall'], response: Optional[Dict[str, Any]], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        table = Table.grid(padding=(0, 1))
        if function_call is not None:
            table.add_row(Text("Function Call", style="bold green"))
            table.add_row(self._format_function_call(function_call))
        if response is not None:
            table.add_row(Text("Response", style="bold blue"))
            table.add_row(self._format_response(response))
        panel_title = "Function Call Group"
        panel = Panel(table, title=panel_title, expand=False)
        console.print(panel)

    def _format_function_call(self, function_call: 'FunctionCall') -> Text:
        # Assuming function_call has 'name' and 'arguments' attributes
        text = Text()
        text.append(f"Name: {getattr(function_call, 'name', '<unknown>')}\n")
        args = getattr(function_call, 'arguments', None)
        if args:
            text.append("Arguments:\n")
            for k, v in args.items():
                text.append(f"  {k}: {v}\n")
        return text

    def _format_response(self, response: Dict[str, Any]) -> Text:
        text = Text()
        for k, v in response.items():
            text.append(f"{k}: {v}\n")
        return text
