
from typing import Any, Dict


class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_calls = []

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if hasattr(obj, 'function_call'):
            self.pending_function_calls.append(obj.function_call)
        else:
            self._flush_pending_function_call(console)
            console.print(obj.description)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        while self.pending_function_calls:
            function_call = self.pending_function_calls.pop(0)
            response = function_call.execute()
            self._render_function_call_group(function_call, response, console)

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        console.print(f"Function Call: {function_call.name}")
        console.print(f"Arguments: {function_call.arguments}")
        console.print(f"Response: {response}")
