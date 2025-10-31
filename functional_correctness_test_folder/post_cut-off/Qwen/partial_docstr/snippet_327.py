
from typing import Any, Dict
from rich.console import Console


class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_calls = {}

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if isinstance(obj, FunctionCall):
            self.pending_function_calls[obj.id] = obj
        elif isinstance(obj, FunctionResponse):
            if obj.id in self.pending_function_calls:
                self._render_function_call_group(
                    self.pending_function_calls.pop(obj.id), obj.response, console)
            else:
                console.print(
                    f"Unmatched response for function call ID: {obj.id}")
        else:
            console.print(f"Unknown event type: {type(obj)}")

    def _flush_pending_function_call(self, console: 'Console') -> None:
        for function_call in self.pending_function_calls.values():
            console.print(
                f"Unmatched function call: {function_call.name} with ID: {function_call.id}")
        self.pending_function_calls.clear()

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        console.print(
            f"Function Call: {function_call.name} with ID: {function_call.id}")
        console.print(f"Response: {response}")
