
from typing import Any


class EventRenderer:

    def __init__(self) -> None:
        self._pending_function_call = None
        self._pending_response = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if hasattr(obj, 'function_call') and hasattr(obj, 'response'):
            # It's a function call event with a response
            if self._pending_function_call is not None:
                self._flush_pending_function_call(console)
            self._pending_function_call = obj.function_call
            self._pending_response = obj.response
        else:
            # Not a function call event, flush any pending
            self._flush_pending_function_call(console)
            if hasattr(obj, 'render'):
                obj.render(console)
            else:
                console.print(str(obj))

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
        console.print(f"Function Call: {function_call}")
        console.print(f"Response: {response}")
