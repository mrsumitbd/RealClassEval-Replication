
from typing import Any, Dict, Optional


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional['FunctionCall'] = None
        self._pending_response: Optional[Dict[str, Any]] = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if isinstance(obj, FunctionCall):
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = obj
        elif isinstance(obj, Response):
            if self._pending_function_call is not None:
                self._pending_response = obj.data
                self._flush_pending_function_call(console)
            else:
                console.print(
                    "Response received without a preceding function call.")
        else:
            console.print(f"Unknown event type: {type(obj)}")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self._pending_function_call is not None and self._pending_response is not None:
            self._render_function_call_group(
                self._pending_function_call, self._pending_response, console)
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        console.print(
            f"Function Call: {function_call.name} with args {function_call.args}")
        console.print(f"Response: {response}")
