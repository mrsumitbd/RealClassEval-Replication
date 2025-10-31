
from typing import Any


class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if self.pending_function_call is not None:
            self._flush_pending_function_call(console)

        if obj.function_call is not None:
            response = obj.response
            self._render_function_call_group(
                obj.function_call, response, console)
        else:
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self.pending_function_call is not None:
            console.print(self.pending_function_call)
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        if self.pending_function_call is not None and self.pending_function_call != function_call:
            self._flush_pending_function_call(console)

        self.pending_function_call = function_call
        # Assuming FunctionCall and Console have the necessary methods and attributes
        # For demonstration purposes, it is assumed that FunctionCall has a __str__ method and Console has a print method
        # In a real scenario, you would need to implement the actual rendering logic here
        # For example:
        # console.print(f"Function Call: {function_call}")
        # console.print(f"Response: {response}")
