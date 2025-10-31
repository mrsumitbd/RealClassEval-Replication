
from typing import Any


class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if self.pending_function_call is not None:
            self._flush_pending_function_call(console)

        if obj.function_call is not None:
            self.pending_function_call = obj.function_call
            self._render_function_call_group(
                obj.function_call, obj.response, console)
        else:
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self.pending_function_call is not None:
            console.print(
                f"Function call {self.pending_function_call.name} completed")
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        console.print(f"Function call: {function_call.name}")
        console.print(f"Arguments: {function_call.arguments}")
        console.print(f"Response: {response}")
        self._flush_pending_function_call(console)
