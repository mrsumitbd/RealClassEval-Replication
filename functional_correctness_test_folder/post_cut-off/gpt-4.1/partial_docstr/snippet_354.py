
from typing import Any


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call = None
        self._pending_response = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        # Assume obj has .type in {"function_call", "function_response", ...}
        # and .data is the payload
        if getattr(obj, 'type', None) == "function_call":
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.data
            self._pending_response = None
        elif getattr(obj, 'type', None) == "function_response":
            if self._pending_function_call is not None:
                self._pending_response = obj.data
                self._flush_pending_function_call(console)
            else:
                # No pending function call, just print response
                console.print(f"[function response] {obj.data}")
        else:
            self._flush_pending_function_call(console)
            # Render other event types directly
            console.print(f"[event] {obj}")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self._pending_function_call is not None:
            self._render_function_call_group(
                self._pending_function_call,
                self._pending_response,
                console
            )
            self._pending_function_call = None
            self._pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        # For demonstration, just print them together
        console.print("[function call]")
        console.print(function_call)
        if response is not None:
            console.print("[function response]")
            console.print(response)
        else:
            console.print("[function response] <no response>")
