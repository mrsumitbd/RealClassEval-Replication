
from typing import Any, Dict


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if hasattr(obj, 'function_call'):
            self._pending_function_call = obj.function_call
        elif hasattr(obj, 'response') and self._pending_function_call:
            self._render_function_call_group(
                self._pending_function_call, obj.response, console)
            self._pending_function_call = None
        elif self._pending_function_call:
            self._flush_pending_function_call(console)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call:
            console.print(
                f"[bold]Function call:[/bold] {self._pending_function_call}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.syntax import Syntax
        from rich.text import Text

        call_text = Text("Function call:\n", style="bold")
        call_text.append(Syntax(str(function_call), "python", theme="monokai"))

        response_text = Text("\nResponse:\n", style="bold")
        response_text.append(Syntax(str(response), "json", theme="monokai"))

        panel = Panel(call_text + response_text,
                      title="Function Call & Response", border_style="blue")
        console.print(panel)
