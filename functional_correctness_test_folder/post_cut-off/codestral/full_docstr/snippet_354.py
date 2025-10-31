
class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self.pending_function_call = None

    def render_event(self, obj: 'Event', console: 'Console') -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if obj.type == 'function_call':
            self._flush_pending_function_call(console)
            self.pending_function_call = obj
        elif obj.type == 'function_response':
            if self.pending_function_call:
                self._render_function_call_group(
                    self.pending_function_call, obj.response, console)
                self.pending_function_call = None

    def _flush_pending_function_call(self, console: 'Console') -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self.pending_function_call:
            console.print(
                f"[bold]Function Call:[/bold] {self.pending_function_call.name}")
            console.print(
                f"[bold]Arguments:[/bold] {self.pending_function_call.arguments}")
            self.pending_function_call = None

    def _render_function_call_group(self, function_call: 'FunctionCall', response: dict[str, Any], console: 'Console') -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.console import Group

        function_call_text = f"[bold]Function Call:[/bold] {function_call.name}\n[bold]Arguments:[/bold] {function_call.arguments}"
        response_text = f"[bold]Response:[/bold] {response}"

        group = Group(
            Panel(function_call_text, title="Function Call", expand=False),
            Panel(response_text, title="Response", expand=False)
        )

        console.print(group)
