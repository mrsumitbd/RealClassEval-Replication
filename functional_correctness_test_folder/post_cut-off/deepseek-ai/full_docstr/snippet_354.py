
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
        elif hasattr(obj, 'response'):
            console.print(obj.response)
        else:
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call:
            console.print(self._pending_function_call)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.columns import Columns
        from rich.text import Text

        call_text = Text(
            f"Call: {function_call.name}\nArgs: {function_call.args}")
        response_text = Text(f"Response: {response}")

        group = Columns([call_text, response_text], expand=True)
        console.print(Panel(group, title="Function Call", border_style="blue"))
