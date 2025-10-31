
class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self.pending_function_call = None
        self.pending_response = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        if isinstance(obj, FunctionCall):
            if self.pending_function_call is not None:
                self._flush_pending_function_call(console)
            self.pending_function_call = obj
        elif isinstance(obj, dict):
            if self.pending_function_call is not None:
                self.pending_response = obj
                self._flush_pending_function_call(console)
            else:
                console.print(obj)

    def _flush_pending_function_call(self, console: 'Console') -> None:
        if self.pending_function_call is not None and self.pending_response is not None:
            self._render_function_call_group(
                self.pending_function_call, self.pending_response, console)
            self.pending_function_call = None
            self.pending_response = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.console import Group

        function_call_text = f"Function Call: {function_call.name}\nArguments: {function_call.arguments}"
        response_text = f"Response: {response}"

        group = Group(function_call_text, response_text)
        panel = Panel(group, title="Function Call and Response", expand=False)
        console.print(panel)
