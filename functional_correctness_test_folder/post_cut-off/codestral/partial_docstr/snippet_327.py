
class EventRenderer:

    def __init__(self) -> None:
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if obj.type == 'function_call':
            self.pending_function_call = obj
        elif obj.type == 'function_call_response':
            if self.pending_function_call:
                self._render_function_call_group(
                    self.pending_function_call, obj.response, console)
                self.pending_function_call = None

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self.pending_function_call:
            self._render_function_call_group(
                self.pending_function_call, None, console)
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        console.print(f"[bold]Function Call:[/bold] {function_call.name}")
        console.print(f"[bold]Arguments:[/bold] {function_call.arguments}")
        if response:
            console.print(f"[bold]Response:[/bold] {response}")
