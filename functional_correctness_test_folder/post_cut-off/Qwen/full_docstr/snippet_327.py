
from typing import Any, Optional
from rich.console import Console
from google.adk.events import Event, FunctionCall


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[FunctionCall] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if isinstance(obj, FunctionCall):
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = obj
        else:
            if self._pending_function_call is not None:
                self._render_function_call_group(
                    self._pending_function_call, obj, console)
                self._pending_function_call = None
            else:
                console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call is not None:
            console.print(
                f"Unmatched Function Call: {self._pending_function_call}")
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        console.print(f"Function Call: {function_call}")
        console.print(f"Response: {response}")
