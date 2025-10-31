
from typing import Any


class EventRenderer:

    def __init__(self) -> None:
        self._pending_function_call = None
        self._pending_response = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if hasattr(obj, 'type') and obj.type == 'function_call':
            # If there is a pending function call, flush it first
            self._flush_pending_function_call(console)
            self._pending_function_call = obj.function_call
            self._pending_response = None
        elif hasattr(obj, 'type') and obj.type == 'function_response':
            if self._pending_function_call is not None:
                self._pending_response = obj.response
                self._flush_pending_function_call(console)
            else:
                # No pending function call, just render response
                self._render_function_call_group(None, obj.response, console)
        else:
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
        if function_call is not None:
            console.print(
                f"Function Call: {function_call.name}({', '.join(f'{k}={v!r}' for k, v in function_call.args.items())})")
        if response is not None:
            console.print(f"Response: {response}")
