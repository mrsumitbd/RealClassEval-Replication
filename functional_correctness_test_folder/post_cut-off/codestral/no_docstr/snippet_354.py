
class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if obj.event == 'function_call':
            if self.pending_function_call is None:
                self.pending_function_call = obj
            else:
                self._flush_pending_function_call(console)
                self.pending_function_call = obj
        elif obj.event == 'function_call_group':
            self._render_function_call_group(
                obj.function_call, obj.response, console)
        else:
            console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self.pending_function_call is not None:
            console.print(self.pending_function_call)
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        console.print(f"Function Call: {function_call}")
        console.print("Response:")
        for key, value in response.items():
            console.print(f"  {key}: {value}")
