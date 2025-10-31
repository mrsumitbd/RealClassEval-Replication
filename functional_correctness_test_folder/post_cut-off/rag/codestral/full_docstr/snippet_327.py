
from typing import Any, Dict, Optional
from rich.console import Console
from google.adk.events import Event, FunctionCall


class EventRenderer:
    '''Stateful renderer that groups function calls with their responses.'''

    def __init__(self) -> None:
        '''Initialize the event renderer.'''
        self._pending_function_call: Optional[FunctionCall] = None

    def render_event(self, obj: Event, console: Console) -> None:
        '''Render the provided google.adk.events.Event to rich.console.'''
        if isinstance(obj, FunctionCall):
            self._flush_pending_function_call(console)
            self._pending_function_call = obj
        elif self._pending_function_call and hasattr(obj, 'response'):
            self._render_function_call_group(
                function_call=self._pending_function_call,
                response=obj.response,
                console=console
            )
            self._pending_function_call = None
        else:
            console.print(obj)

    def _flush_pending_function_call(self, console: Console) -> None:
        '''Render any pending function call that hasn't been paired with a response.'''
        if self._pending_function_call:
            console.print(self._pending_function_call)
            self._pending_function_call = None

    def _render_function_call_group(self, function_call: FunctionCall, response: Dict[str, Any], console: Console) -> None:
        '''Render function call and response together in a grouped panel.'''
        from rich.panel import Panel
        from rich.text import Text

        call_text = Text.assemble(
            ("Function Call: ", "bold"),
            (f"{function_call.name}", "italic green")
        )
        response_text = Text.assemble(
            ("Response: ", "bold"),
            (f"{response}", "blue")
        )

        panel_content = Text.assemble(
            call_text, "\n", response_text
        )

        console.print(
            Panel(panel_content, title="Function Call Group", expand=False))
