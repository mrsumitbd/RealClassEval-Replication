
from typing import Any, Dict


class EventRenderer:

    def __init__(self) -> None:
        self._pending_function_calls = []

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if hasattr(obj, 'function_call'):
            self._pending_function_calls.append(obj.function_call)
        else:
            self._flush_pending_function_call(console)
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if not self._pending_function_calls:
            return
        function_call = self._pending_function_calls.pop(0)
        self._render_function_call_group(
            function_call, function_call.response, console)

    def _render_function_call_group(self, function_call: 'FunctionCall', response: Dict[str, Any], console: 'Console') -> None:
        console.print(f"[bold]Function Call:[/bold] {function_call.name}")
        console.print(f"[bold]Arguments:[/bold] {function_call.arguments}")
        if response:
            console.print(f"[bold]Response:[/bold] {response}")
